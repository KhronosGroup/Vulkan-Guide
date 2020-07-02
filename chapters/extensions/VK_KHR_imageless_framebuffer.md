# VK_KHR_imageless_framebuffer

> Promoted to core in Vulkan 1.2

When creating a `VkFramebuffer` you normally need to pass the `VkImageView`s being used in `VkFramebufferCreateInfo::pAttachments`. The Vulkan Working Group came to the conclusion that this information is not fully needed by implementations when creating the framebuffer. By removing this requirement, the hope is to allow more flexibility in how they are used and avoiding the need for many of the confusing compatibility rules.

To use an imageless `VkFramebuffer`

- Make sure the implementation has support for it
  - By querying `VkPhysicalDeviceImagelessFramebufferFeatures::imagelessFramebuffer` or having at least a Vulkan 1.2 device
- Set the `VK_FRAMEBUFFER_CREATE_IMAGELESS_BIT` in `VkFramebufferCreateInfo::flags`
- Include a `VkFramebufferAttachmentsCreateInfo` struct in the `VkFramebufferCreateInfo::pNext`
- When starting the RenderPass, pass in a `VkRenderPassAttachmentBeginInfo` struct into `VkRenderPassBeginInfo::pNext` with the compatible attachments
