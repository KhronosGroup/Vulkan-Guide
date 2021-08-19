# Cleanup Extensions

> These are extensions that are unofficially called "cleanup extension". The Vulkan Guide defines them as cleanup extensions due to their nature of only adding a small bit of functionality or being very simple, self-explanatory extensions in terms of their purpose.

## VK_KHR_driver_properties

> Promoted to core in Vulkan 1.2

This extension adds more information to query about each implementation. The [VkDriverId](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkDriverId) will be a registered vendor's ID for the implementation. The [VkConformanceVersion](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkConformanceVersion) displays which version of [the Vulkan Conformance Test Suite](../vulkan_cts.md) the implementation passed.

## VK_EXT_host_query_reset

> Promoted to core in Vulkan 1.2

This extension allows an application to call `vkResetQueryPool` from the host instead of needing to setup logic to submit `vkCmdResetQueryPool` since this is mainly just a quick write to memory for most implementations.

## VK_KHR_separate_depth_stencil_layouts

> Promoted to core in Vulkan 1.2

This extension allows an application when using a depth/stencil format to do an image translation on each the depth and stencil separately. Starting in Vulkan 1.2 this functionality is required for all implementations.

## VK_KHR_depth_stencil_resolve

> Promoted to core in Vulkan 1.2

This extension adds support for automatically resolving multisampled depth/stencil attachments in a subpass in a similar manner as for color attachments.

For more information please check out the GDC presentation. ([slides](https://www.khronos.org/assets/uploads/developers/presentations/Vulkan-Depth-Stencil-Resolve-GDC-Mar19.pdf) and [video](https://www.youtube.com/watch?v=GnnEmJFFC7Q&t=1980s))

## VK_EXT_separate_stencil_usage

> Promoted to core in Vulkan 1.2

There are formats that express both the usage of depth and stencil, but there was no way to list a different usage for them. The `VkImageStencilUsageCreateInfo` now lets an application pass in a separate `VkImageUsageFlags` for the stencil usage of an image. The depth usage is the original usage passed into `VkImageCreateInfo::usage` and without using `VkImageStencilUsageCreateInfo` the stencil usage will be the same as well.

A good use case of this is when using the [VK_KHR_image_format_list](./VK_KHR_image_format_list.md) extension. This provides a way for the application to more explicitly describe the possible image views of their `VkImage` at creation time. This allows some implementations to possibly do implementation dependent optimization depending on the usages set.

## VK_KHR_dedicated_allocation

> Promoted to core in Vulkan 1.1

Normally applications allocate large chunks for `VkDeviceMemory` and then suballocate to various buffers and images. There are times where it might be better to have a dedicated allocation for `VkImage` or `VkBuffer`. An application can pass `VkMemoryDedicatedRequirements` into `vkGetBufferMemoryRequirements2` or `vkGetImageMemoryRequirements2` to find out if a dedicated allocation is preferred or required. When dealing with external memory it will often require a dedicated allocation.

## VK_EXT_sampler_filter_minmax

> Promoted to core in Vulkan 1.2

By default, Vulkan samplers using linear filtering return a filtered texel value produced by computing a weighted average of a collection of texels in the neighborhood of the texture coordinate provided. This extension provides a new sampler parameter which allows applications to produce a filtered texel value by computing a component-wise minimum (`VK_SAMPLER_REDUCTION_MODE_MIN`) or maximum (`VK_SAMPLER_REDUCTION_MODE_MAX`) of the texels that would normally be averaged. This is similar to [GL EXT_texture_filter_minmax](https://www.khronos.org/registry/OpenGL/extensions/EXT/EXT_texture_filter_minmax.txt).

## VK_KHR_sampler_mirror_clamp_to_edge

> Promoted to core in Vulkan 1.2

This extension adds a new sampler address mode (`VK_SAMPLER_ADDRESS_MODE_MIRROR_CLAMP_TO_EDGE`) that effectively uses a texture map twice as large as the original image in which the additional half of the new image is a mirror image of the original image. This new mode relaxes the need to generate images whose opposite edges match by using the original image to generate a matching “mirror image”. This mode allows the texture to be mirrored only once in the negative `s`, `t`, and `r` directions.

## VK_EXT_4444_formats and VK_EXT_ycbcr_2plane_444_formats

These extensions add new `VkFormat` that were not originally in the spec

# Maintenance Extensions

The maintenance extensions add a collection of minor features that were intentionally left out or overlooked from the original Vulkan 1.0 release.

Currently, there are 3 maintenance extensions, all of which were bundled in Vulkan 1.1 as core. All the details for each are well defined in the extension appendix page.

- [VK_KHR_maintenance1](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VK_KHR_maintenance1)
- [VK_KHR_maintenance2](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VK_KHR_maintenance2)
- [VK_KHR_maintenance3](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VK_KHR_maintenance3)

# pNext Expansions

There have been a few times where the Vulkan Working Group realized that some structs in the original 1.0 Vulkan spec were missing the ability to be extended properly due to missing `sType`/`pNext`.

Keeping backward compatibility between versions is very important, so the best solution was to create an extension to amend the mistake. These extensions are mainly new structs, but also need to create new function entry points to make use of the new structs.

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

## Example

Using `VK_KHR_bind_memory2` as an example, instead of using the standard `vkBindImageMemory`

```cpp
// VkImage images[3]
// VkDeviceMemory memories[2];

vkBindImageMemory(myDevice, images[0], memories[0], 0);
vkBindImageMemory(myDevice, images[1], memories[0], 64);
vkBindImageMemory(myDevice, images[2], memories[1], 0);
```

They can now be batched together

[source,c++]
```cpp
// VkImage images[3];
// VkDeviceMemory memories[2];

VkBindImageMemoryInfo infos[3];
infos[0] = {VK_STRUCTURE_TYPE_BIND_IMAGE_MEMORY_INFO, NULL, images[0], memories[0], 0};
infos[1] = {VK_STRUCTURE_TYPE_BIND_IMAGE_MEMORY_INFO, NULL, images[1], memories[0], 64};
infos[2] = {VK_STRUCTURE_TYPE_BIND_IMAGE_MEMORY_INFO, NULL, images[2], memories[1], 0};

vkBindImageMemory2(myDevice, 3, infos);
```

Some extensions such as `VK_KHR_sampler_ycbcr_conversion` expose structs that can be passed into the `pNext`

```cpp
VkBindImagePlaneMemoryInfo plane_info[2];
plane_info[0] = {VK_STRUCTURE_TYPE_BIND_IMAGE_PLANE_MEMORY_INFO, NULL, VK_IMAGE_ASPECT_PLANE_0_BIT};
plane_info[1] = {VK_STRUCTURE_TYPE_BIND_IMAGE_PLANE_MEMORY_INFO, NULL, VK_IMAGE_ASPECT_PLANE_1_BIT};

// Can now pass other extensions structs into the pNext missing from vkBindImagemMemory()
VkBindImageMemoryInfo infos[2];
infos[0] = {VK_STRUCTURE_TYPE_BIND_IMAGE_MEMORY_INFO, &plane_info[0], image, memories[0], 0};
infos[1] = {VK_STRUCTURE_TYPE_BIND_IMAGE_MEMORY_INFO, &plane_info[1], image, memories[1], 0};

vkBindImageMemory2(myDevice, 2, infos);
```

## It is fine to not use these

Unless an application need to make use of one of the extensions that rely on the above extensions, it is normally ok to use the original function/structs still.

One possible way to handle this is as followed:

```cpp
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
