# Translation Layer Extensions

There is a class of extensions that were only created to allow efficient ways for [translation layers](../portability_initiative.md#translation-layer) to map to Vulkan.

This includes replicating legacy behavior that is challenging for drivers to implement efficiently. This functionality is **not** considered forward looking, and is **not** expected to be promoted to a KHR extension or to core Vulkan.

Unless this is needed for translation, it is **highly recommended** that developers use alternative techniques of using the GPU to achieve the same functionality.

## VK_EXT_depth_clip_enable

The depth clip enable functionality is specified differently from D3D11 and Vulkan. Instead of `VkPipelineRasterizationStateCreateInfo::depthClampEnable`, D3D11 has [DepthClipEnable (D3D12_RASTERIZER_DESC)](https://docs.microsoft.com/en-us/windows/desktop/api/d3d11/ns-d3d11-d3d11_rasterizer_desc), which only affects the viewport clip of depth values before rasterization and does not affect the depth clamp that always occurs in the output merger stage of the D3D11 graphics pipeline.

## VK_EXT_provoking_vertex

Vulkan's defaults convention for provoking vertex is "first vertex" while OpenGL’s defaults convention is "last vertex".

## VK_EXT_transform_feedback

Everything needed for transform feedback can be done via a compute shader in Vulkan. There is also a great [blog by Jason Ekstrand](http://jason-blog.jlekstrand.net/2018/10/transform-feedback-is-terrible-so-why.html) on why transform feedback is terrible and should be avoided.
