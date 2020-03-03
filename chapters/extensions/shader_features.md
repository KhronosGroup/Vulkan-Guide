# Shader Features

There is a class of extensions whose purpose is just to interact with the SPIR-V interface of Vulkan. This can be things such as exposing SPIR-V capabilities, valid types supported, etc. It is important to remember that SPIR-V is an intermediate language and not an API, it relies on an API, such as Vulkan, to expose what features are available to the application at runtime.

There are various reasons why every part of SPIR-V was not exposed to Vulkan 1.0. Overtime the Vulkan Working Group has identified use cases where it makes sense to expose a new SPIR-V feature.

Some of the following extensions were added alongside a SPIR-V extension. For example, the `VK_KHR_8bit_storage` extension was created in parallel with `SPV_KHR_8bit_storage`. The Vulkan extension allows an application to query for support in the implementation. The SPIR-V extension is there to define the changes made to the SPIR-V IR.

# Example Workflow

This example is to illustrate the pieces of using shader features extension. What this example is doing is not the point, this is for understanding the logistics involved. This example will be using `VK_KHR_8bit_storage` as an example, but details about the extension can be found below in its [own section below](#vk_khr_8bit_storage-and-vk_khr_16bit_storage).

1. Check if the Vulkan extension is supported or if has been promoted in the Vulkan version being used
    - For this case, an application would query `VK_KHR_8bit_storage` or check if Vulkan 1.2 is supported
2. Enable the extension when creating the `VkDevice` unless it is the case where the extension is in core and the implementation doesn't expose the extension.
    - If the implementation exposes the extension as well as being in core, it is still suggested to enable it at device creation.
3. Query the Physical Device feature struct exposed by the Vulkan extension.
    - `VkPhysicalDevice8BitStorageFeatures::uniformAndStorageBuffer8BitAccess` or `VkPhysicalDeviceVulkan12Features::uniformAndStorageBuffer8BitAccess` in this case.
4. If using a high-level shading language, such as GLSL, make any changes needed.
    -  In this example, we will need to use the GLSL extension to convert
    ```
    #version 450

    // Without 8bit storage
    layout (set = 0, binding = 0) readonly buffer StorageBuffer {
        uint data; // 0x0000AABB
    } ssbo;

    void main() {
        uint a = ssbo.data & 0x0000FF00;
        uint b = ssbo.data & 0x000000FF;
    }
    ```
    to
    ```
    #version 450
    #extension GL_EXT_shader_8bit_storage : enable

    // With 8bit storage
    layout (set = 0, binding = 0) readonly buffer StorageBuffer {
        uint8_t dataA; // 0xAA
        uint8_t dataB; // 0xBB
    } ssbo;

    void main() {
        uint a = uint(ssbo.dataA);
        uint b = uint(ssbo.dataB);
    }
    ```
5. Convert to SPIR-V and make sure any SPIR-V extensions involved are supported. Tools such as `glslang` and `SPIRV-Tools` will handle this for an application.
    - In this example, when converting the updated shader to SPIR-V the assembly will describe the features being used
    ```
    OpCapability Shader
    OpCapability UniformAndStorageBuffer8BitAccess
    OpExtension  "SPV_KHR_8bit_storage"
    ```
6. Alter any Vulkan code needed to match with the SPIR-V interface changes
    - In this example, the only change is that the storage buffer descriptor only is 2 bytes large now instead of originally 4 bytes, but the content of the 2 bytes of data would remain the same.

# VK_KHR_spirv_1_4

> Promoted to core in Vulkan 1.2

This extension is designed for a Vulkan 1.1 implementations to expose the SPIR-V 1.4 feature set. Vulkan 1.1 only requires SPIR-V 1.3 and some use cases were found where an implementation might not upgrade to Vulkan 1.2, but still want to offer SPIR-V 1.4 features.

# VK_KHR_8bit_storage and VK_KHR_16bit_storage

> [SPV_KHR_8bit_storage](http://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_8bit_storage.html)
>
> [SPV_KHR_16bit_storage](http://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_16bit_storage.html)
>
> [GLSL - GL_EXT_shader_16bit_storage](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_shader_16bit_storage.txt) defines both

Both `VK_KHR_8bit_storage` (promoted in Vulkan 1.2) and `VK_KHR_16bit_storage` (promoted in Vulkan 1.1) were added to allow the ability to use small values as input or output to a SPIR-V storage object. Prior to these extensions, all UBO, SSBO, and push constants needed to consume at least 4 bytes. With this, an application can now use 8-bit or 16-bit values directly from a buffer. It is also commonly paired with the use of `VK_KHR_shader_float16_int8` as this extension only deals with the storage interfaces.

# VK_KHR_shader_float16_int8

>  Promoted to core in Vulkan 1.2
>
> [GLSL - GL_EXT_shader_explicit_arithmetic_types](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_shader_explicit_arithmetic_types.txt)

This extension allows the use of 8-bit integer types or 16-bit floating-point types for arithmetic operations. This does not allow for 8-bit integer types or 16-bit floating-point types in any shader input and output interfaces and therefore is commonly paired with the use of `VK_KHR_8bit_storage` and `VK_KHR_16bit_storage`.

# VK_KHR_shader_atomic_int64

> Promoted to core in Vulkan 1.2
>
> [GLSL - GL_EXT_shader_atomic_int64](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_shader_atomic_int64.txt)

This extension allows for 64bit atomic operations

An example would involve using `uint64_t atomicAnd(inout uint64_t mem, uint64_t data);` in GLSL and having it mapped down to the `OpAtomicAnd` in SPIR-V

# VK_KHR_shader_float_controls

> Promoted to core in Vulkan 1.2
>
> [SPV_KHR_float_controls](http://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_float_controls.html)

This extension allows the ability to set how rounding of floats are handled. The `VkPhysicalDeviceFloatControlsProperties` shows the full list of features that can be queried. This is useful when converting OpenCL kernels to Vulkan.

# VK_KHR_storage_buffer_storage_class

> Promoted to core in Vulkan 1.1
>
> [SPV_KHR_storage_buffer_storage_class](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_storage_buffer_storage_class.html)

Originally SPIR-V combined both UBO and SSBO into the 'Uniform' storage classes and differentiated them only through extra decorations. Because some hardware treats UBO an SSBO as two different storage objects, the SPIR-V wanted to reflect that. This extension serves the purpose of extending SPIR-V to have a new `StorageBuffer` class.

# VK_KHR_variable_pointers

> Promoted to core in Vulkan 1.1
>
> [SPV_KHR_variable_pointers](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_variable_pointers.html)

A `Variable pointer` is defined in SPIR-V as
> A pointer of logical pointer type that results from one of the following instructions: `OpSelect`, `OpPhi`, `OpFunctionCall`, `OpPtrAccessChain`, ` OpLoad`, or `OpConstantNull`

When this extension is enabled invocation-private pointers can be dynamic and non-uniform. Without this extension a variable pointer must be selected from pointers pointing into the same structure or be `OpConstantNull`.

This extension has two level to it. The first is the `variablePointersStorageBuffer` feature bit which allows implementation supports the use of variable pointers into a SSBO only. The `variablePointers` feature bit allows the use of variable pointers outside the SSBO as well.

# VK_KHR_uniform_buffer_standard_layout

> Promoted to core in Vulkan 1.2

This extension allows the use of std430 memory layout in UBOs. More information about [std140 and std430 memory layouts](https://www.khronos.org/opengl/wiki/Interface_Block_(GLSL)#Memory_layout) and [Vulkan Standard Buffer Layout Interface](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#interfaces-resources-standard-layout) can be found outside this guide. These memory layout changes are only applied to `Uniforms` as other storage items such as Push Constants and SSBO already allow for std430 style layouts.

# VK_KHR_relaxed_block_layout

> Promoted to core in Vulkan 1.1

This extension allows implementations to indicate they can support more variation in block `Offset` decorations. This comes up when using std430 memory layout where a `vec3` (which is 12 bytes) is still defined as a 16 byte alignment. With relaxed block layout an application can fit a `float` on either side of the `vec3` and maintain the 16 byte alignment between them. For more information see [Offset and Stride Assignment](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#interfaces-resources-layout) for details.

```
// SPIR-V offsets WITHOUT relaxed block layout
layout (set = 0, binding = 0) buffer StorageBuffer {
    vec3 a;  // Offset: 0
    float b; // Offset: 16
} ssbo;

// SPIR-V offsets WITH relaxed block layout
layout (set = 0, binding = 0) buffer StorageBuffer {
    vec3 a;  // Offset: 0
    float b; // Offset: 12
} ssbo;


// SPIR-V offsets WITHOUT relaxed block layout
layout (set = 0, binding = 0) buffer StorageBuffer {
    float b; // Offset: 0
    vec3 a;  // Offset: 16
} ssbo;

// SPIR-V offsets WITH relaxed block layout
layout (set = 0, binding = 0) buffer StorageBuffer {
    float b; // Offset: 0
    vec3 a;  // Offset: 4
} ssbo;
```

`VK_KHR_relaxed_block_layout` can also be seen as a subset of `VK_EXT_scalar_block_layout`

> Make sure to set `--relax-block-layout` when running the SPIR-V Validator

# VK_EXT_scalar_block_layout

> Promoted to core in Vulkan 1.2
>
> [GLSL - GL_EXT_scalar_block_layout](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_scalar_block_layout.txt)

This extension allows all storage types to be aligned solely based on the size of their components, without additional requirements.

An example would be where an application straddles the 16-byte boundary. With scalar block layout the following GLSL/SPIR-V would be legal to use

```
#version 450
#extension GL_EXT_scalar_block_layout : enable

layout (scalar, set = 0, binding = 0) buffer StorageBuffer {
    vec3 a; // Offset: 0
    vec2 b; // Offset: 12
    vec2 c; // Offset: 20
    vec3 d; // Offset: 28
} ssbo;

... translated to

OpMemberDecorate 11(StorageBuffer) 0 Offset 0
OpMemberDecorate 11(StorageBuffer) 1 Offset 12
OpMemberDecorate 11(StorageBuffer) 2 Offset 20
OpMemberDecorate 11(StorageBuffer) 3 Offset 28
```

> Make sure to set `--scalar-block-layout` when running the SPIR-V Validator


# VK_KHR_vulkan_memory_model

> Promoted to core in Vulkan 1.2
>
> [Comparing the Vulkan SPIR-V memory model to C++‘s](https://www.khronos.org/blog/comparing-the-vulkan-spir-v-memory-model-to-cs)

The [Vulkan Memory Model](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#memory-model) formally defines how to synchronize memory accesses to the same memory locations performed by multiple shader invocations and this extension exposes a boolean to let implementations to indicate support for it. This is important because with many things targeting Vulkan/SPIR-V it is important that any memory transfer operations an application might attempt to optimize doesn't break across implementations.

# VK_KHR_shader_subgroup_extended_types

> Promoted to core in Vulkan 1.2
>
> [GLSL_EXT_shader_subgroup_extended_types](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_shader_subgroup_extended_types.txt)

This extension allows subgroup operations to use 8-bit integer, 16-bit integer, 64-bit integer, 16-bit floating-point, and vectors of these types in group operations with subgroup scope if the implementation supports the types already.

For example, if an implementation supports 8-bit integers an application can now use the GLSL `genI8Type subgroupAdd(genI8Type value);` call which will get mapped to `OpGroupNonUniformFAdd` in SPIR-V.

# VK_EXT_shader_viewport_index_layer

> Promoted to core in Vulkan 1.2
>
> [SPV_EXT_shader_viewport_index_layer](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/EXT/SPV_EXT_shader_viewport_index_layer.html)
>
> [GLSL - GL_ARB_shader_viewport_layer_array](https://www.khronos.org/registry/OpenGL/extensions/ARB/ARB_shader_viewport_layer_array.txt)

This extension adds the `ViewportIndex`, `Layer` built-in for exporting from vertex or tessellation shaders.

In GLSL these are represented by `gl_ViewportIndex` and `gl_Layer` built-ins.

# VK_KHR_shader_draw_parameters

> Promoted to core in Vulkan 1.1
>
> [SPV_KHR_shader_draw_parameters](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_shader_draw_parameters.html)
>
> [GLSL - GL_ARB_shader_draw_parameters](https://www.khronos.org/registry/OpenGL/extensions/ARB/ARB_shader_draw_parameters.txt)

This extension adds the `BaseInstance`, `BaseVertex`, and `DrawIndex` built-in for vertex shaders. This was added as there are legitimate use cases for both inclusion and exclusion of the `BaseVertex` or `BaseInstance` parameters in `VertexId` and `InstanceId`, respectively.

In GLSL these are represented by `gl_BaseInstanceARB`, `gl_BaseVertexARB` and `gl_BaseInstanceARB` built-ins.

# VK_EXT_shader_stencil_export

> [SPV_EXT_shader_stencil_export](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/EXT/SPV_EXT_shader_stencil_export.html)
>
> [GLSL - GL_ARB_shader_stencil_export](https://www.khronos.org/registry/OpenGL/extensions/ARB/ARB_shader_stencil_export.txt)

This extension allows a shader to generate the stencil reference value per invocation. When stencil testing is enabled, this allows the test to be performed against the value generated in the shader.

In GLSL this is represented by a `out int gl_FragStencilRefARB` built-in.

# VK_EXT_shader_demote_to_helper_invocation

> [SPV_EXT_demote_to_helper_invocation](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/EXT/SPV_EXT_demote_to_helper_invocation.html)
>
> [GLSL - GL_EXT_demote_to_helper_invocation](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_demote_to_helper_invocation.txt)

This extension was created to help with matching the HLSL `discard` instruction in SPIR-V by adding a `demote` keyword. When using `demote` in a fragment shader invocation it becomes a helper invocation. Any stores to memory after this instruction are suppressed and the fragment does not write outputs to the framebuffer.

# VK_KHR_shader_clock

> [SPV_KHR_shader_clock](http://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_shader_clock.html)
>
> [GLSL - GL_EXT_shader_realtime_clock](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_shader_realtime_clock.txt)

This extension allows the shader to read the value of a monotonically incrementing counter provided by the implementation. This can be used as one possible method for debugging by tracking the order of when an invocation executes the instruction. It is worth noting that the addition of the `OpReadClockKHR` alters the shader one might want to debug. This means there is a certain level of accuracy representing the order as if the instructions did not exists.

# VK_EXT_subgroup_size_control

This extension was created due to some implementation having more than one subgroup size and Vulkan originally only exposing a single subgroup size.

For example, if an implementation only has support for subgroups of size `4` and `16` before they would have had to expose only one size, but now can expose both. This allows applications to potentially control the hardware at a finer granularity for implementations that expose multiple subgroup sizes.

# VK_EXT_shader_subgroup_ballot and VK_EXT_shader_subgroup_vote

`VK_EXT_shader_subgroup_ballot` and `VK_EXT_shader_subgroup_vote` were the original efforts to expose subgroups in Vulkan. If an application is using Vulkan 1.1 or greater, there is no need to use these extensions and instead use the core API to query for subgroup support.

For more information about the current subgroup support, there is a great [Khronos blog post](https://www.khronos.org/blog/vulkan-subgroup-tutorial) as well as a presentation from Vulkan Developer Day 2018 ([slides](https://www.khronos.org/assets/uploads/developers/library/2018-vulkan-devday/06-subgroups.pdf) and [video](https://www.youtube.com/watch?v=8MyqQLu_tW0)). GLSL support can be found in the [GL_KHR_shader_subgroup](https://github.com/KhronosGroup/GLSL/blob/master/extensions/khr/GL_KHR_shader_subgroup.txt) extension
