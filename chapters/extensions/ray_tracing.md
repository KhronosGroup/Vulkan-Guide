# Ray Tracing

A set of five interrelated extensions provide ray tracing support in the Vulkan API.

* [VK_KHR_acceleration_structure](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_acceleration_structure.html)
* [VK_KHR_ray_tracing_pipeline](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_ray_tracing_pipeline.html)
* [VK_KHR_ray_query](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_ray_query.html)
* [VK_KHR_pipeline_library](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_pipeline_library.html)
* [VK_KHR_deferred_host_operations](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_deferred_host_operations.html)

Additional SPIR-V and GLSL extensions also expose the necessary programmable functionality for shaders:

* [SPV_KHR_ray_tracing](http://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_ray_tracing.html)
* [SPV_KHR_ray_query](http://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_ray_query.html)
* [GLSL_EXT_ray_tracing](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_ray_tracing.txt)
* [GLSL_EXT_ray_query](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_ray_query.txt)
* [GLSL_EXT_ray_flags_primitive_culling](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_ray_flags_primitive_culling.txt)

## VK_KHR_acceleration_structure

Acceleration structures are an implementation-dependent opaque representation
of geometric objects, which are used for ray tracing.
By building objects into acceleration structures, ray tracing can be performed
against a known data layout, and in an efficient manner.
The `VK_KHR_acceleration_structure` extension introduces functionality to build
and copy acceleration structures, along with functionality to support
serialization to/from memory.

Acceleration structures are required for both ray pipelines
(`VK_KHR_ray_tracing_pipeline`) and ray queries (`VK_KHR_ray_query`). 

To create an acceleration structure:

* Populate an instance of `VkAccelerationStructureBuildGeometryInfoKHR` with
  the acceleration structure type, geometry types, counts, and maximum sizes.
  The geometry data does not need to be populated at this point.
* Call `vkGetAccelerationStructureBuildSizesKHR` to get the memory size
  requirements to perform a build.
* Allocate buffers of sufficient size to hold the acceleration structure
  (`VkAccelerationStructureBuildSizesKHR::accelerationStructureSize`) and build
  scratch buffer (`VkAccelerationStructureBuildSizesKHR::buildScratchSize`)
* Call `vkCreateAccelerationStructureKHR` to create an acceleration structure
  at a specified location within a buffer
* Call `vkCmdBuildAccelerationStructuresKHR` to build the acceleration structure.
  The previously populated `VkAccelerationStructureBuildGeometryInfoKHR` should
  be used as a parameter here, along with the destination acceleration structure
  object, build scratch buffer, and geometry data pointers (for vertices,
  indices and transforms)

## VK_KHR_ray_tracing_pipeline

The `VK_KHR_ray_tracing_pipeline` extension introduces ray tracing pipelines.
This new form of rendering pipeline is independent of the traditional
rasterization pipeline. Ray tracing pipelines utilize a dedicated set of shader
stages, distinct from the traditional vertex/geometry/fragment stages. Ray tracing
pipelines also utilize dedicated commands to submit rendering work
(`vkCmdTraceRaysKHR` and `vkCmdTraceRaysIndirectKHR`). These commands can be
regarded as somewhat analagous to the drawing commands in traditional 
rasterization pipelines (`vkCmdDraw` and `vkCmdDrawIndirect`).

To trace rays:

* Bind a ray tracing pipeline using `vkCmdBindPipeline` with
  `VK_PIPELINE_BIND_POINT_RAY_TRACING_KHR`
* Call `vkCmdTraceRaysKHR` or `vkCmdTraceRaysIndirectKHR`

Ray tracing pipelines introduce several new shader domains. These are described
below:

![](https://www.khronos.org/assets/uploads/blogs/2020-The-ray-tracing-mechanism-achieved-through-the-five-shader-stages-2.jpg "Ray Tracing Shaders")

  * Ray generation shader represents the starting point for ray tracing. The ray tracing commands 
    (`vkCmdTraceRaysKHR` and `vkCmdTraceRaysIndirectKHR`) launch a grid of shader invocations,
    similar to compute shaders. A ray generation shader constructs rays and begins tracing via
    the invocation of traceRayEXT(). Additionally, it processes the results from the hit group.
   
  * Closest hit shaders are executed when the ray intersects the closest geometry. An application
    can support any number of closest hit shaders. They are typically used for carrying out
    lighting calculations and can recursively trace additional rays.

  * Miss shaders are executed instead of a closest hit shader when a ray does not intersect any
    geometry during traversal. A common use for a miss shader is to sample an environment map.

  * The built-in intersection test is a ray-triangle test. Intersection shaders allow for custom
    intersection handling.

  * Similar to the closest hit shader, any-hit shaders are executed after an intersection is
    reported. The difference is that an any-hit shader are be invoked for any intersection in
    the ray interval defined by [tmin, tmax] and not the closest one to the origin of the ray.
    The any-hit shader is used to filter an intersection and therefore is often used to
    implement alpha-testing.

## VK_KHR_ray_query

The `VK_KHR_ray_query` extension provides support for tracing rays from all
shader types, including graphics, compute, and ray tracing pipelines.

Ray query requires that ray traversal code is explicitly included within the
shader. This differs from ray tracing pipelines, where ray generation,
intersection testing and handling of ray-geometry hits are represented as
separate shader stages. Consequently, whilst ray query allows rays to be traced
from a wider range of shader stages, it also restricts the range of optimizations
that a Vulkan implementation might apply to the scheduling and tracing of rays.

The extension does not introduce additional API entry-points. It simply provides
API support for the related SPIR-V and GLSL extensions (`SPV_KHR_ray_query` and
`GLSL_EXT_ray_query`).

The functionality provided by `VK_KHR_ray_query` is complementary to that
provided by `VK_KHR_ray_tracing_pipeline`, and the two extensions can be used
together.

```glsl
rayQueryEXT rq;

rayQueryInitializeEXT(rq, accStruct, gl_RayFlagsNoneEXT, 0, origin, tMin, direction, tMax);

while(rayQueryProceedEXT(rq)) {
	if (rayQueryGetIntersectionTypeEXT(rq, false) == gl_RayQueryCandidateIntersectionTriangleEXT) {
		//...
		rayQueryConfirmIntersectionEXT(rq);
	}
}

if (rayQueryGetIntersectionTypeEXT(rq, true) == gl_RayQueryCommittedIntersectionNoneEXT) {
	//...
}
```

## VK_KHR_pipeline_library

`VK_KHR_pipeline_library` introduces pipeline libraries. A pipeline library is
a special pipeline that was created using the `VK_PIPELINE_CREATE_LIBRARY_BIT_KHR`
and cannot be bound and used directly. Instead, these are pipelines that
represent a collection of shaders, shader groups and related state which can be
linked into other pipelines.

`VK_KHR_pipeline_library` does not introduce any new API functions directly, or
define how to create a pipeline library. Instead, this functionality is left to
other extensions which make use of the functionality provided by
`VK_KHR_pipeline_library`.
Currently, the only example of this is `VK_KHR_ray_tracing_pipeline`. 
`VK_KHR_pipeline_library` was defined as a separate extension to allow for the
possibility of using the same functionality in other extensions in the future
without introducing a dependency on the ray tracing extensions.

To create a ray tracing pipeline library:

* Set `VK_PIPELINE_CREATE_LIBRARY_BIT_KHR` in `VkRayTracingPipelineCreateInfoKHR::flags`
  when calling `vkCreateRayTracingPipelinesKHR`

To link ray tracing pipeline libraries into a full pipeline:

* Set `VkRayTracingPipelineCreateInfoKHR::pLibraryInfo` to point to an instance
  of `VkPipelineLibraryCreateInfoKHR`
* Populate `VkPipelineLibraryCreateInfoKHR::pLibraries` with the pipeline
  libraries to be used as inputs to linking, and set `VkPipelineLibraryCreateInfoKHR::libraryCount`
  to the appropriate value

## VK_KHR_deferred_host_operations

`VK_KHR_deferred_host_operations` introduces a mechanism for distributing expensive
CPU tasks across multiple threads. Rather than introduce a thread pool into Vulkan
drivers, `VK_KHR_deferred_host_operations` is designed to allow an application to
create and manage the threads.

As with `VK_KHR_pipeline_library`, `VK_KHR_deferred_host_operations` was defined
as a separate extension to allow for the possibility of using the same functionality
in other extensions in the future without introducing a dependency on the ray
tracing extensions. 

Only operations that are specifically noted as supporting deferral may be deferred.
Currently the only operations which support deferral are `vkCreateRayTracingPipelinesKHR`,
`vkBuildAccelerationStructuresKHR`, `vkCopyAccelerationStructureKHR`,
`vkCopyMemoryToAccelerationStructureKHR`, and `vkCopyAccelerationStructureToMemoryKHR`

To request that an operation is deferred:

* Create a `VkDeferredOperationKHR` object by calling `vkCreateDeferredOperationKHR`
* Call the operation that you wish to be deferred, passing the `VkDeferredOperationKHR`
  as a parameter.
* Check the `VkResult` returned by the above operation:
  * `VK_OPERATION_DEFERRED_KHR` indicates that the operation was successfully
    deferred
  * `VK_OPERATION_NOT_DEFERRED_KHR` indicates that the operation successfully
    completed immediately
  * Any error value indicates that an error occurred

To join a thread to a deferred operation, and contribute CPU time to progressing
the operation:

* Call `vkDeferredOperationJoinKHR` from each thread that you wish to participate
  in the operation
* Check the `VkResult` returned by `vkDeferredOperationJoinKHR`:
  * `VK_SUCCESS` indicates that the operation is complete
  * `VK_THREAD_DONE_KHR` indicates that there is no more work to assign to the
    calling thread, but that other threads may still have some additional work to
    complete. The current thread should not attempt to re-join by calling
    `vkDeferredOperationJoinKHR` again
  * `VK_THREAD_IDLE_KHR` indicates that there is *temporarily* no work to assign
    to the calling thread, but that additional work may become available in the
    future. The current thread may perform some other useful work on the calling
    thread, and re-joining by calling `vkDeferredOperationJoinKHR` again later
    may prove beneficial

After an operation has completed (i.e. `vkDeferredOperationJoinKHR` has returned
`VK_SUCCESS`), call `vkGetDeferredOperationResultKHR` to get the result of the
operation.
