# VK_EXT_memory_priority

Memory management is an important part of Vulkan. The `VK_EXT_memory_priority` extension was designed to allow an application to prevent important allocations from being moved to slower memory.

This extension can be explained with an example of two applications (yours and another process on the host machine). Over time the applications both attempt to consume the limited device heap memory.

![VK_EXT_memory_priority_overview](images/VK_EXT_memory_priority_overview.png)

In this situation, the allocation from your application is still present, just possibly on slower memory (implementation might have moved it to host visible memory until it is needed again).

The decision of **what** memory will get moved is implementation defined. Let's now imagine this is your application's memory usage

![VK_EXT_memory_priority_app](images/VK_EXT_memory_priority_app.png)

As we can see, there was some memory the application felt was more important to always attempt to keep in fast memory.

The `VK_EXT_memory_priority` extension makes this very easy. When allocating memory, an application just needs to add `VkMemoryPriorityAllocateInfoEXT` to `VkMemoryAllocateInfo::pNext`. From here the `VkMemoryPriorityAllocateInfoEXT::priority` value can be set with a value between `0.0` and `1.0` (where `0.5`) is the default. This allows the application to help the implementation make a better guess if the above situation occurs.

# Suggestions

- Make sure the extension is supported.
- Remember this is a **hint** to the implementation and an application should still try to budget properly prior to using this.
- Always measure memory bottlenecks instead of making assumptions when possible.
- Any memory being written to will have a good chance of being a high priority.
    - Render targets (Ex: Framebuffer's output attachments) are usually important to set too high priority
- View high priority memory as having "high frequency access" and "low latency tolerance"
    - Ex: Vertex buffers, which remain stable across multiple frames, have each value accessed only once, and typically are forgiving for access latency, are usually a good candidate for lower priorities.