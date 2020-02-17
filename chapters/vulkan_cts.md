# Vulkan CTS

The Vulkan Conformance Tests Suite (CTS) is a set of tests used to verify the conformance of an implementation. A conformant implementation shows that it has successfully passed CTS and it is a valid implementation of Vulkan. A [list of conformant products](https://www.khronos.org/conformance/adopters/conformant-products/vulkan) is publicly available.

Any company with a conformant implementation may freely use the publicly released Vulkan specification to create a product. All implementations of the Vulkan API must be tested for conformance in the [Khronos Vulkan Adopter Program](https://www.khronos.org/adopters) before the Vulkan name or logo may be used in association with an implementation of the API.

The [Vulkan CTS source code](https://github.com/KhronosGroup/VK-GL-CTS/tree/master/external/vulkancts) is freely available and anyone is free to create and add a new test to the Vulkan CTS as long as they follow the [Contributing Wiki](https://github.com/KhronosGroup/VK-GL-CTS/wiki/Contributing).

![vulkan_cts_overview.png](../images/vulkan_cts_overview.png)

An application can query the version of CTS passed for an implementation using the [VkConformanceVersion](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkConformanceVersion) property via the `VK_KHR_driver_properties` extension (this was promoted to core in Vulkan 1.2).