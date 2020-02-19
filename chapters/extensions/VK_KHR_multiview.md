# VK_KHR_multiview

> Promoted to core in Vulkan 1.1
>
> [SPV_KHR_multiview](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_multiview.html)
>
> [GLSL - GL_EXT_multiview](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_multiview.txt)

Multiview is a rendering technique originally designed for VR where it is more efficient to record a single set of commands to be executed with slightly different behavior for each "view". This is all done during Renderpass creation with the `VkRenderPassMultiviewCreateInfo` passed into `VkRenderPassCreateInfo::pNext`.

This extension is paired with [SPV_KHR_multiview](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_multiview.html) which adds a new `ViewIndex` built-in type to shaders that allow shaders to control what to do for each view. If using GLSL there is also a [GL_EXT_multiview](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_multiview.txt) extension that introduces a `highp int gl_ViewIndex;` built-in variable for vertex, tessellation, geometry, and fragment shaders.

For more information about multiview there are great articles online from [NVIDIA](https://devblogs.nvidia.com/turing-multi-view-rendering-vrworks/) and [ARM](https://community.arm.com/developer/tools-software/graphics/b/blog/posts/optimizing-virtual-reality-understanding-multiview) on this topic.