# What is Vulkan?

> Vulkan is a new generation graphics and compute API that provides high-efficiency, cross-platform access to modern GPUs used in a wide variety of devices from PCs and consoles to mobile phones and embedded platforms.

Vulkan is not a company, nor language, but rather a way for developers to program their modern GPU hardware in a cross-platform and cross-vendor fashion. The Khronos Group is a member-driven consortium that created and maintains Vulkan.

## Vulkan at its core

At the core, Vulkan is an [API Specification](https://www.khronos.org/registry/vulkan/#apispecs) that conformant hardware implementations follow. The public specification is generated from the [./xml/vk.xml](https://github.com/KhronosGroup/Vulkan-Docs/blob/master/xml/vk.xml) Vulkan Registry file in the official public copy of the Vulkan Specification repo found at [Vulkan-Doc](https://github.com/KhronosGroup/Vulkan-Docs). Documentation of the [XML schema](https://www.khronos.org/registry/vulkan/specs/1.1/registry.html) is also available.

The Khronos Group, along with the Vulkan Specification, releases [C99](http://www.open-std.org/jtc1/sc22/wg14/www/standards) [header files](https://github.com/KhronosGroup/Vulkan-Headers/tree/master/include/vulkan) generated from the [API Registry](https://www.khronos.org/registry/vulkan/#apiregistry) that developers can use to interface with the Vulkan API.

For those who might not work with C code, there are various [language](https://github.com/KhronosGroup/Khronosdotorg/blob/master/api/vulkan/resources.md#language-bindings) [bindings](https://github.com/vinjn/awesome-vulkan#bindings) out there.

## Vulkan and OpenGL

Some developers might be aware of the other Khronos Group standard [OpenGL](https://www.khronos.org/opengl/) which is also a 3D Graphics API. Vulkan is not a direct replacement for OpenGL, but rather an explicit API that allows for more explicit control of the GPU.

![what_is_vulkan_compared_to_gl.png](../images/what_is_vulkan_compared_to_gl.png)

Vulkan puts more work and responsibility into the application. Not every developer will want to make that extra investment, but those that do so correctly can find power and performance improvements.

![what_is_vulkan_decision.png](../images/what_is_vulkan_decision.png)

## Using helping libraries

While some developers may want to try using Vulkan with no help, it is common to use some lighter libraries in your development flow to help abstract some of the more tedious aspect of Vulkan. Here are some [libraries](https://github.com/KhronosGroup/Khronosdotorg/blob/master/api/vulkan/resources.md#libraries) to [help with development](https://github.com/vinjn/awesome-vulkan#libraries)

![what_is_vulkan_layer](../images/what_is_vulkan_layer.png)