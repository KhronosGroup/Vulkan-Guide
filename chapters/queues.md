# Queues

> Further resources for queues from [AMD](https://gpuopen.com/learn/concurrent-execution-asynchronous-queues/) and [NVIDIA](https://www.khronos.org/assets/uploads/developers/library/2016-vulkan-devday-uk/9-Asynchonous-compute.pdf)

A `VkQueue` is what an application submits work to, normally in the form of `VkCommandBuffer` objects or [sparse bindings](./sparse_resources.md).

Command buffers submitted to a `VkQueue` start in order, but are allowed to proceed independently after that and complete out of order.

Command buffers submitted to different queues are unordered relative to each other unless you explicitly synchronize them with a `VkSemaphore`.

You can only submit work to a `VkQueue` from one thread at a time, but different threads can submit work to different a `VkQueue` simultaneously.

The concept of a `vkQueue` is implementationed defined. Some hardware have multiple hardware queues and submitting work to multiple `vkQueue` will proceed independently and concurrently in the hardware. Some implementation will do some scheduling at a kernel driver level before being submitted to the hardware. There is no current way in Vulkan to expose the exact details how each `vkQueue` is mapped to the implementation.

> Not all applications will require or benefit from mulitple queues. It is reasonable for an application to have a single "universal" graphics supported queue to submit all the work to the GPU.

# Queue Family

There are various types of operations a `VkQueue` can support. A "Queue Family" just describes a set of `VkQueue` that have common properties and support the same functionality, as advertised in `VkQueueFamilyProperties`.

The following are the queue operations found in [VkQueueFlagBits](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VkQueueFlagBits.html):

- `VK_QUEUE_GRAPHICS_BIT` used for `vkCmdDraw*` and graphic pipeline commands.
- `VK_QUEUE_COMPUTE_BIT` used for `vkCmdDispatch*` and `vkCmdTraceRays*` and compute pipeline related commands.
- `VK_QUEUE_TRANSFER_BIT` used for all transfer commands.
    - [VK_PIPELINE_STAGE_TRANSFER_BIT](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VkPipelineStageFlagBits.html) in the Spec describes "transfer commands".
    - Queue Families with only `VK_QUEUE_TRANSFER_BIT` are usually for using [DMA](https://en.wikipedia.org/wiki/Direct_memory_access) to asynchronously transfer data between host and device memory on discrete GPUs, so transfers can be done concurrently with independent graphics/compute operations.
    - `VK_QUEUE_GRAPHICS_BIT` and `VK_QUEUE_COMPUTE_BIT` can always implicitly accept `VK_QUEUE_TRANSFER_BIT` commands.
- `VK_QUEUE_SPARSE_BINDING_BIT` used for binding [sparse resources](./sparse_resources.md) to memory with `vkQueueBindSparse`.
- `VK_QUEUE_PROTECTED_BIT` used for [protected memory](./protected.md).
- `VK_QUEUE_VIDEO_DECODE_BIT_KHR` and `VK_QUEUE_VIDEO_ENCODE_BIT_KHR` used with [Vulkan Video](https://www.khronos.org/blog/an-introduction-to-vulkan-video?mc_cid=8052312abe&mc_eid=64241dfcfa).

## Knowing which Queue Family is needed

Each operation in the Vulkan Spec has a "Supported Queue Types" section generated from the [vk.xml](https://github.com/KhronosGroup/Vulkan-Docs/blob/master/xml/vk.xml) file. The following is 3 different examples of what it looks like in the Spec:

![queues_cmd_dispatch.png](../images/queues_cmd_draw.png)

![queues_cmd_dispatch.png](../images/queues_cmd_dispatch.png)

![queues_cmd_dispatch.png](../images/queues_cmd_executecommands.png)

## Querying for Queue Family

The following is the simplest logic needed if an application only wants a single graphics `vkQueue`

```cpp
uint32_t count = 0;
vkGetPhysicalDeviceQueueFamilyProperties(physicalDevice, &count, nullptr);
std::vector<VkQueueFamilyProperties> properties(count);
vkGetPhysicalDeviceQueueFamilyProperties(physicalDevice, &count, properties.data());

// Vulkan requires an implementation to expose at least 1 queue family with graphics
uint32_t graphicsQueueFamilyIndex;

for (uint32_t i = 0; i < count; i++) {
    if ((properties[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) != 0) {
        // This Queue Family support graphics
        graphicsQueueFamilyIndex = i;
        break;
    }
}
```

## Creating and getting a Queue

Unlike other handles such as `VkDevice`, `VkBuffer`, `VkDeviceMemory`, there is **no** `vkCreateQueue` or `vkAllocateQueue`. Instead, the driver is in charge of creating and destroying the `VkQueue` handles during `vkCreateDevice`/`vkDestroyDevice` time.

The following examples will use the hypothetical implementation which support 3 `VkQueue` from 2 Queue Families:

![queues_hypothetical.png](../images/queues_hypothetical.png)

The following is an example how to create all 3 `VkQueue` with the logical device:

```cpp
VkDeviceQueueCreateInfo queueCreateInfo[2];
queueCreateInfo[0].queueFamilyIndex = 0; // Transfer
queueCreateInfo[0].queueCount = 1;
queueCreateInfo[1].queueFamilyIndex = 1; // Graphics
queueCreateInfo[1].queueCount = 2;

VkDeviceCreateInfo deviceCreateInfo   = {};
deviceCreateInfo.pQueueCreateInfos    = queueCreateInfo;
deviceCreateInfo.queueCreateInfoCount = 2;

vkCreateDevice(physicalDevice, &deviceCreateInfo, nullptr, &device);
```

After creating the `VkDevice` the application can use `vkGetDeviceQueue` to get the `vkQueue` handles

```cpp
vkQueue graphicsQueue0 = VK_NULL_HANDLE;
vkQueue graphicsQueue1 = VK_NULL_HANDLE;
vkQueue transferQueue0 = VK_NULL_HANDLE;

// Can be obtained in any order
vkGetDeviceQueue(device, 0, 0, &transferQueue0); // family 0 - queue 0
vkGetDeviceQueue(device, 1, 1, &graphicsQueue1); // family 1 - queue 1
vkGetDeviceQueue(device, 1, 0, &graphicsQueue0); // family 1 - queue 0
```
