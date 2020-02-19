# VK_KHR_depth_stencil_resolve

> Promoted to core in Vulkan 1.2

This extension was created to support doing resolve on depth and stencil images. The main use case for this is tile-based architectures where doing MSAA on depth and stencil targets is expensive due to not having a way to keep the memory in the tiler memory.

A common question is what type of equation does one perform when resolving a multi-sampled depth or stencil image. The full list of possible equations is defined in the [VkResolveModeFlagBits](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkResolveModeFlagBits) enum. The `VK_RESOLVE_MODE_SAMPLE_ZERO_BIT` is the only mode that is required by all implementations (from supporting the extension or being Vulkan 1.2 or higher), but some may expose more.

For more information, there is a great GDC talk about this extension ([video](https://www.youtube.com/watch?v=GnnEmJFFC7Q&feature=youtu.be&t=1983) and [slides](https://www.khronos.org/assets/uploads/developers/library/2019-gdc/Vulkan-Depth-Stencil-Resolve-GDC-Mar19.pdf)).