# VK_KHR_image_format_list

> Promoted to core in Vulkan 1.2

Some implementations have cases where they can do optimizations for certain formats. The issue comes when an application sets `VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT` in `VkImageCreateInfo` and there is no way the implementation knows if it's one of the formats to apply an implementation dependent optimization too. By using the `VkImageFormatListCreateInfo` struct and listing the possible formats the implementation only needs to check against the subset of formats listed and still enable an implementation dependent optimization.

If the application is not using the `VK_IMAGE_CREATE_MUTABLE_FORMAT_BIT` to create images, then there is no need to be concerned with this extension.