# VK_KHR_draw_indirect_count

This extension was promoted in Vulkan 1.2 and allows an application to source the number of draw calls for indirect draw calls from a buffer. This enables applications to generate arbitrary amounts of draw commands and execute them without host intervention.

The `vkCmdDrawIndirectCount` and `vkCmdDrawIndexedIndirectCount` function can be used if the extension is supported or the `VkPhysicalDeviceVulkan12Features::drawIndirectCount` feature bit is true in a Vulkan 1.2 or greater version.

The following diagram is to visualize the difference between `vkCmdDraw`, `vkCmdDrawIndirect`, and `vkCmdDrawIndirectCount`.

![VK_KHR_draw_indirect_count example](images/VK_KHR_draw_indirect_count_example.png)