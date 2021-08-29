# Enabling Features

This section goes over the logistics for enabling features.

## Category of Features

All features in Vulkan can be categorized/found in 3 sections

1. Core 1.0 Features
    - These are the set of features that were available from the initial 1.0 release of Vulkan. The list of features can be found in [VkPhysicalDeviceFeatures](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkPhysicalDeviceFeatures)
2. Future Core Version Features
    - With Vulkan 1.1 and 1.2 some new features were added to the core version of Vulkan. To keep the size of `VkPhysicalDeviceFeatures` backward compatible, new structs were created to hold the grouping of features.
    - [VkPhysicalDeviceVulkan11Features](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkPhysicalDeviceVulkan11Features)
    - [VkPhysicalDeviceVulkan12Features](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkPhysicalDeviceVulkan12Features)
3. Extension Features
    - Sometimes extensions contain features in order to enable certain aspects of the extension. These are easily found as they are all labeled as `VkPhysicalDevice[[ExtensionName]]Features`

## How to Enable the Features

All features must be enabled at `VkDevice` creation time inside the [VkDeviceCreateInfo](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkDeviceCreateInfo) struct.

> Don't forget to query first with `vkGetPhysicalDeviceFeatures` or `vkGetPhysicalDeviceFeatures2`

For the Core 1.0 Features, this is as simple as setting `VkDeviceCreateInfo::pEnabledFeatures` with the features desired to be turned on.

```cpp
VkPhysicalDeviceFeatures features = {};
vkGetPhysicalDeviceFeatures(physical_device, &features);

// Logic if feature is not supported
if (features.robustBufferAccess == VK_FALSE) {
}

VkDeviceCreateInfo info = {};
info.pEnabledFeatures = &features;
```

For **all features**, including the Core 1.0 Features, use `VkPhysicalDeviceFeatures2` to pass into `VkDeviceCreateInfo.pNext`

```cpp
VkPhysicalDeviceShaderDrawParametersFeatures ext_feature = {};

VkPhysicalDeviceFeatures2 physical_features2 = {};
physical_features2.pNext = &ext_feature;

vkGetPhysicalDeviceFeatures2(physical_device, &physical_features2);

// Logic if feature is not supported
if (ext_feature.shaderDrawParameters == VK_FALSE) {
}

VkDeviceCreateInfo info = {};
info.pNext = &physical_features2;
```

The same works for the "Future Core Version Features" too.

```cpp
VkPhysicalDeviceVulkan11Features features11 = {};

VkPhysicalDeviceFeatures2 physical_features2 = {};
physical_features2.pNext = &features11;

vkGetPhysicalDeviceFeatures2(physical_device, &physical_features2);

// Logic if feature is not supported
if (features11.shaderDrawParameters == VK_FALSE) {
}

VkDeviceCreateInfo info = {};
info.pNext = &physical_features2;
```
