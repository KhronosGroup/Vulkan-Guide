# Image Creation

The `vkCreateImage` and its `VkImageCreateInfo` contain a lot of information and there is a class of extensions aimed towards this important API call.

# VK_KHR_image_format_list

> Promoted to core in Vulkan 1.2

Some implementations have cases where they can do optimizations for certain formats. The issue comes when an application sets `VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT` in `VkImageCreateInfo` and there is no way the implementation knows if it's one of the formats to apply an implementation dependent optimization too. By using the `VkImageFormatListCreateInfo` struct and listing the possible formats the implementation only needs to check against the subset of formats listed and still enable an implementation dependent optimization.

If the application is not using the `VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT` to create images, then there is no need to be concerned with this extension.

# VK_EXT_separate_stencil_usage

> Promoted to core in Vulkan 1.2

There are formats that express both the usage of depth and stencil, but there was no way to list a different usage for them. The `VkImageStencilUsageCreateInfo` now lets an application pass in a separate `VkImageUsageFlags` for the stencil usage of an image. The depth usage is the original usage passed into `VkImageCreateInfo::usage` and without using `VkImageStencilUsageCreateInfo` the stencil usage will be the same as well.

A good use case of this is when using the `VK_KHR_image_format_list` extension. This provides a way for the application to more explicitly describe the possible image views of their `VkImage` at creation time. This allows some implementations to possibly do implementation dependent optimization depending on the usages set.