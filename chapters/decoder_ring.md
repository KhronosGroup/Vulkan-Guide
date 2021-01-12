# Vulkan Decoder Ring

This section provides a mapping between the Vulkan term for a concept and the terminology used in other APIs. It is organized in alphabetical order by Vulkan term. If you are searching for the Vulkan equivalent of a concept used in an API you know, you can find the term you know in this list and then search the [Vulkan specification](./vulkan_spec.md) for the corresponding Vulkan term.

> Not everything will be a perfect 1:1 match, the goal is to give a rough idea where to start looking in the spec.

**Vulkan**|**GL,GLES**|**DirectX**|**Metal**
:-----:|:-----:|:-----:|:-----:
buffer device address||GPU virtual address|
buffer view, texel buffer|texture buffer|typed buffer SRV, typed buffer UAV|texture buffer
color attachments|color attachments|render target|color attachments or render target
command buffer|part of context, display list, NV_command_list|command list|command buffer
command pool|part of context|command allocator|command queue
conditional rendering|conditional rendering|predication|
depth/stencil attachment|depth Attachment and stencil Attachment|depth/stencil view|depth attachment and stencil attachment, depth render target and stencil render target
descriptor||descriptor|argument
descriptor pool||descriptor heap|heap
descriptor set||descriptor table|argument buffer
descriptor set layout binding, push descriptor||root parameter|argument in shader parameter list
device group|implicit (E.g. SLI,CrossFire)|multi-adapter device|peer group
device memory||heap|placement heap
event||split barrier|
fence|fence, sync|`ID3D12Fence::SetEventOnCompletion`|completed handler, `-[MTLCommandBuffer waitUntilComplete]`
fragment shader|fragment shader|pixel shader|fragment shader or fragment function
fragment shader interlock|[GL_ARB_fragment_shader_interlock](https://www.khronos.org/registry/OpenGL/extensions/ARB/ARB_fragment_shader_interlock.txt)|rasterizer order view (ROV)|raster order group
framebuffer|framebuffer object|collection of resources|
heap||pool|
image|texture and renderbuffer|texture|texture
image layout||resource state|
image tiling||image layout, swizzle|
image view|texture view|render target view, depth/stencil view, shader resource view, unordered access view|texture view
interface matching (`in`/`out`)|varying ([removed in GLSL 4.20](https://www.khronos.org/registry/OpenGL/specs/gl/GLSLangSpec.4.20.pdf))|Matching semantics|
invocation|invocation|thread, lane|thread, lane
layer||slice|slice
logical device|context|device|device
memory type|automatically managed, [texture storage hint](https://www.khronos.org/registry/OpenGL/extensions/APPLE/APPLE_texture_range.txt), [buffer storage](https://www.khronos.org/registry/OpenGL/extensions/ARB/ARB_buffer_storage.txt)|heap type, CPU page property|storage mode, CPU cache mode
multiview rendering|multiview rendering|view instancing|vertex amplification
physical device||adapter, node|device
pipeline|state and program or program pipeline|pipeline state|pipeline state
pipeline barrier, memory barrier|texture barrier, memory barrier|resource barrier|texture barrier, memory barrier
pipeline layout||root signature|
queue|part of context|command queue|command queue
semaphore|fence, sync|fence|fence, event
shader module|shader object|resulting `ID3DBlob` from `D3DCompileFromFile`|shader library
shading rate attachment||shading rate image|rasterization rate map
sparse block|sparse block|tile|sparse tile
sparse image|sparse texture|reserved resource (D12), tiled resource (D11)|sparse texture
storage buffer|shader storage buffer|raw or structured buffer UAV|buffer in `device` address space
subgroup|subgroup|wave|SIMD-group, quadgroup
surface|HDC, GLXDrawable, EGLSurface|window|layer
swapchain|Part of HDC, GLXDrawable, EGLSurface|swapchain|layer
swapchain image|default framebuffer||drawable texture
tessellation control shader|tessellation control shader|hull shader|tessellation compute kernel
tessellation evaluation shader|tessellation evaluation shader|domain shader|post-tessellation vertex shader
timeline semaphore||D3D12 fence|event
transform feedback|transform feedback|stream-out|
uniform buffer|uniform buffer|constant buffer views (CBV)|buffer in `constant` address space
workgroup|workgroup|threadgroup|threadgroup
