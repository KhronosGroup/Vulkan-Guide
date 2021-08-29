# Subgroups

The Vulkan Spec defines subgroups as:

> A set of shader invocations that can synchronize and share data with each other efficiently. In compute shaders, the local workgroup is a superset of the subgroup.

For many implementations, a subgroup is the groups of invocations that run the same instruction at once. Subgroups allow for a shader writer to work at a finer granularity than a single workgroup.

## Resources

For more detailed information about subgroups there is a great [Khronos blog post](https://www.khronos.org/blog/vulkan-subgroup-tutorial) as well as a presentation from Vulkan Developer Day 2018 ([slides](https://www.khronos.org/assets/uploads/developers/library/2018-vulkan-devday/06-subgroups.pdf) and [video](https://www.youtube.com/watch?v=8MyqQLu_tW0)). GLSL support can be found in the [GL_KHR_shader_subgroup](https://github.com/KhronosGroup/GLSL/blob/master/extensions/khr/GL_KHR_shader_subgroup.txt) extension.


## Subgroup size

It is important to also realize the size of a subgroup can be dynamic for an implementation. Some implementations may dispatch shaders with a varying subgroup size for different subgroups. As a result, they could implicitly split a large subgroup into smaller subgroups or represent a small subgroup as a larger subgroup, some of whose invocations were inactive on launch. Using [VK_EXT_subgroup_size_control](./extensions/shader_features.md#vk_ext_subgroup_size_control) an application can query for this information.

## Checking for support

With Vulkan 1.1, all the information for subgroups is found in `VkPhysicalDeviceSubgroupProperties`

```cpp
VkPhysicalDeviceSubgroupProperties subgroupProperties;

VkPhysicalDeviceProperties2KHR deviceProperties2;
deviceProperties2.sType      = VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PROPERTIES_2;
deviceProperties2.pNext      = &subgroupProperties;
vkGetPhysicalDeviceProperties2(physicalDevice, &deviceProperties2);

// Example of checking if supported in fragment shader
if ((subgroupProperties.supportedStages & VK_SHADER_STAGE_FRAGMENT_BIT) != 0) {
    // fragment shaders supported
}

// Example of checking if ballot is supported
if ((subgroupProperties.supportedOperations & VK_SUBGROUP_FEATURE_BALLOT_BIT) != 0) {
    // ballot subgroup operations supported
}
```

### Guaranteed support

For supported stages, the Vulkan Spec guarantees the following support:

> **supportedStages** will have the **VK_SHADER_STAGE_COMPUTE_BIT** bit set if any of the physical device’s queues support **VK_QUEUE_COMPUTE_BIT**.

For supported operations, the Vulkan Spec guarantees the following support:

> **supportedOperations** will have the **VK_SUBGROUP_FEATURE_BASIC_BIT** bit set if any of the physical device’s queues support **VK_QUEUE_GRAPHICS_BIT** or **VK_QUEUE_COMPUTE_BIT**.