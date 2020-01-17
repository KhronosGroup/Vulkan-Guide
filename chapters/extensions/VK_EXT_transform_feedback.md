# VK_EXT_transform_feedback

The `VK_EXT_transform_feedback` extension's primary purpose is to support translation layers from other 3D APIs (such as OpenGL and OpenGL ES). This includes replicating legacy behavior that is challenging for drivers to implement efficiently. This functionality is **not** considered forward looking, and is **not** expected to be promoted to a KHR extension or to core Vulkan.`

Unless this is needed for translation, it is **highly recommended** that developers use alternative techniques of using the GPU to process and capture vertex data.