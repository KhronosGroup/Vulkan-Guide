# Translation Layer Extensions

There is a class of extensions that were only created to allow efficient ways for [translation layers](../portability_initiative.md#translation-layer) to map to Vulkan.

This includes replicating legacy behavior that is challenging for drivers to implement efficiently. This functionality is **not** considered forward looking, and is **not** expected to be promoted to a KHR extension or to core Vulkan.

Unless this is needed for translation, it is **highly recommended** that developers use alternative techniques of using the GPU to achieve the same functionality.

# VK_EXT_transform_feedback

Everything needed for transform feedback can be done via a compute shader in Vulkan. There is also a great [blog by Jason Ekstrand](http://jason-blog.jlekstrand.net/2018/10/transform-feedback-is-terrible-so-why.html) on why transform feedback is terrible and should be avoided.