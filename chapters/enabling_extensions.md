# Enabling Extensions

This section goes over the logistics for enabling extensions.

## Check for support

An application can [query the physical device](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#extendingvulkan-extensions) first to check if the extension is **supported** with `vkEnumerateInstanceExtensionProperties` or `vkEnumerateDeviceExtensionProperties`.

```
// Simple example
uint32_t count = 0;
vkEnumerateDeviceExtensionProperties(physicalDevice, nullptr, &count, nullptr);
std::vector<VkExtensionProperties> extensions(count);
vkEnumerateDeviceExtensionProperties(physicalDevice, nullptr, &count, extensions.data());

// Checking for support of VK_KHR_bind_memory2
for (uint32_t i = 0; i < count; i++) {
    if (strcmp(VK_KHR_BIND_MEMORY_2_EXTENSION_NAME, extensions[i].extensionName) == 0) {
        break; // VK_KHR_bind_memory2 is supported
    }
}
```

## Enable the Extension

Even if the extension is **supported** by the implementation, it is **undefined behavior** to use the functionality of the extension unless it is **enabled** at `VkInstance` or `VkDevice` creation time. Here is an example of what is needed to enable an extension such as `VK_KHR_driver_properties`:

```
// VK_KHR_get_physical_device_properties2 is a required instance extension for VK_KHR_driver_properties
std::vector<const char*> instance_extensions;
instance_extensions.push_back(VK_KHR_GET_PHYSICAL_DEVICE_PROPERTIES_2_EXTENSION_NAME);

VkInstanceCreateInfo instance_create_info  = {};
instance_create_info.enabledExtensionCount   = static_cast<uint32_t>(instance_extensions.size());
instance_create_info.ppEnabledExtensionNames = instance_extensions.data();
vkCreateInstance(&instance_create_info, nullptr, &myInstance));

// ...

std::vector<const char*> device_extensions;
device_extensions.push_back(VK_KHR_DRIVER_PROPERTIES_EXTENSION_NAME);

VkDeviceCreateInfo device_create_info      = {};
device_create_info.enabledExtensionCount   = static_cast<uint32_t>(device_extensions.size());
device_create_info.ppEnabledExtensionNames = device_extensions.data();
vkCreateDevice(physicalDevice, &device_create_info, nullptr, &myDevice);
```

## Promotion Process

When minor versions of [Vulkan are released](./vulkan_release_summary.md), some extensions are [promoted as defined in the spec](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#extendingvulkan-compatibility-promotion). The goal of promotion is to have applications not need to query for **support** and **enable** extended functionality that the Vulkan Working Group has decided is important enough to be in the core Vulkan spec.

An example would be something such as `VK_KHR_get_physical_device_properties2` which is used for most other extensions. In Vulkan 1.0, an application has to query for support of `VK_KHR_get_physical_device_properties2` before being able to call a function such as `vkGetPhysicalDeviceFeatures2KHR`. Starting in Vulkan 1.1, the `vkGetPhysicalDeviceFeatures2` function is guaranteed to be supported.

### Promotion Change of Behavior

It is important to realize there is a subtle difference for **some** extension that are promoted. [The spec describes](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#extendingvulkan-compatibility-promotion) how promotion **can** involve minor changes such as in the extension's "Feature advertisement/enablement". To best describe the subtlety of this, `VK_KHR_8bit_storage` can be used as a use case.

The [Vulkan spec describes the change](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#_differences_relative_to_vk_khr_8bit_storage) for `VK_KHR_8bit_storage` for Vulkan 1.2 where it states:

> If the VK_KHR_8bit_storage extension is not supported, support for the SPIR-V StorageBuffer8BitAccess capability in shader modules is optional.

"not supported" here refers to the fact an implementation might support Vulkan 1.2, but if an application queries `vkEnumerateDeviceExtensionProperties` it is possible that `VK_KHR_8bit_storage` will not be in the result.
- If `VK_KHR_8bit_storage` is found in `vkEnumerateDeviceExtensionProperties` then the `storageBuffer8BitAccess` feature is **guaranteed** to be supported.
- If `VK_KHR_8bit_storage` is **not** found in `vkEnumerateDeviceExtensionProperties` then the `storageBuffer8BitAccess` feature **might** be supported and can be checked by querying `VkPhysicalDeviceVulkan12Features::storageBuffer8BitAccess`.

The list of all feature changes to promoted extensions can be found in the [version appendix of the spec](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#versions).