# VK_KHR_draw_indirect_count

> Promoted to core in Vulkan 1.2

This extension allows an application to source the number of draw calls for indirect draw calls from a `VkBuffer`. This enables applications to generate arbitrary amounts of draw commands and execute them without host intervention.

The `vkCmdDrawIndirectCount` and `vkCmdDrawIndexedIndirectCount` function can be used if the extension is supported or checking the `VkPhysicalDeviceVulkan12Features::drawIndirectCount` feature bit.

The following diagram is to visualize the difference between `vkCmdDraw`, `vkCmdDrawIndirect`, and `vkCmdDrawIndirectCount`.

![VK_KHR_draw_indirect_count example](images/VK_KHR_draw_indirect_count_example.png)
