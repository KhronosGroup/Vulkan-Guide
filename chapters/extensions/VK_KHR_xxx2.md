# VK_KHR_*2

There have been a few times where the Vulkan Working Group realized that some structs in the original 1.0 Vulkan spec were missing the ability to be extended properly due to missing `sType`/`pNext`.

Keeping backward compatibility between versions is very important, so the best solution was to create an extension to amend the mistake. These extensions mainly new structs, but also need to create new function entry points to make use of the new structs.

The current list of extensions that fit this category are:
- `VK_KHR_get_memory_requirements2`
    - Added to core in Vulkan 1.1
- `VK_KHR_get_physical_device_properties2`
    - Added to core in Vulkan 1.1
- `VK_KHR_bind_memory2`
    - Added to core in Vulkan 1.1
- `VK_KHR_create_renderpass2`
    - Added to core in Vulkan 1.2

All of these are very simple extensions and were promoted to core in their respective versions to make it easier to use without having to query for their support.

> `VK_KHR_get_physical_device_properties2` has additional functionality as it adds the ability to query feature support for extensions and newer Vulkan versions. It has become a requirement for most other Vulkan extensions because of this.

# It is fine to not use these

Unless you need to make use of one of the extensions that rely on the above extensions, it is normally ok to use the original function/structs still.

One possible way to handle this is as followed:

```
void HandleVkBindImageMemoryInfo(const VkBindImageMemoryInfo* info) {
    // ...
}

//
// Entry points into tool/implementation
//
void vkBindImageMemory(VkDevice device,
                       VkImage image,
                       VkDeviceMemory memory,
                       VkDeviceSize memoryOffset)
{
    VkBindImageMemoryInfo info;
    // original call doesn't have a pNext or sType
    info.sType = VK_STRUCTURE_TYPE_BIND_IMAGE_MEMORY_INFO;
    info.pNext = nullptr;

    // Match the rest of struct the same
    info.image = image;
    info.memory = memory;
    info.memoryOffset = memoryOffset;

    HandleVkBindImageMemoryInfo(&info);
}

void vkBindImageMemory2(VkDevice device,
                        uint32_t bindInfoCount, const
                        VkBindImageMemoryInfo* pBindInfos)
{
    for (uint32_t i = 0; i < bindInfoCount; i++) {
        HandleVkBindImageMemoryInfo(pBindInfos[i]);
    }
}
```