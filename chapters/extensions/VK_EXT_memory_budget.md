# VK_EXT_memory_budget

Memory management is an important part of Vulkan. The `VK_EXT_memory_budget` extension was designed to allow some implementations to advertise even more fine grained details about the device memory heaps.

There are two important concepts this extension tries to help with

- For example, a device memory heap might expose it supports `2GB`, but after 1.5GB has been allocated the platform may try to reclaim memory - potentially resulting in allocations migrating to slower memory, OOM conditions, or even process termination.
- Another process on the machine might also be attempting to use the device memory as well.

`VkPhysicalDeviceMemoryBudgetPropertiesEXT::heapBudget` presents how much memory the **current process** can use before possible allocation failure or performance degradation.

`VkPhysicalDeviceMemoryBudgetPropertiesEXT::heapUsage` will display the **current process** estimated heap usage.

With this information, the idea is for an application at some interval (once per frame, per few seconds, etc) to query `heapBudget` and `heapUsage`. From here the application can notice if they are over budget and decide how it wants to handle the memory situation (free it, move to host memory, changing mipmap levels, etc). A suggestion is to look at [VK_EXT_memory_priority](VK_EXT_memory_priority.md) too as it was designed to help with this part of memory management.