# Common Pitfalls for new Vulkan Developers

This is a short list of commom assumptions and traps developers new to Vulkan can make.  

### Validation Layers

During developement, try to ensure that the Validation Layers are enabled. They are an invaluable tool for catching mistakes while using the Vulkan API. Parameter checking, object lifetimes, and threading violations all are part of the provided error checks. A way to reassure that they are enabled is to verify if the text "Debug Messenger Added" is in the output stream. More info can be found in the [Vulkan SDK](https://vulkan.lunarg.com/doc/sdk) documentation. It is first on the list because it is the first line of defense and should help reduce the time spent discovering where the mistake was made.

### Resource duplication per swapchain image

A common technique to increase throughput is to make multiple instances of a resource, where each instance can be used while rendering a different frame. The swapchain is one such example, as it contains multiple images. This can lead to the assumption that the number of instances each resource has should be the same as the swapchain image count. The issue with this assumption is that very few resources need to be duplicated the same amount as the swapchain image count. While it is useful for some things, for example the number of semaphores used to signal when a swapchain image is available, it is worth understanding which resources have one to one relationships and which don't.

### Recording command buffers  

A common assumption when first learning about command buffers is that reusing them is paramount and that re-recording them every frame is costly. While it appear counterintuitive, there is often a greater cost in reuse than simply recording new command buffers each frame. The main cost is the additional complexity for managing dynamicism, frustum culling, and many other graphical effects. Many of the approaches used to reduce command buffer recording add non trivial state management or undue complexity to the rendering architecture. Therefore, especially in simpler situations, the cost of re-recording every frame is reasonable. Developers still concerned can and should profile command buffer recording to make better informed decisions about the best approach for their application.

### Multiple pipelines

A graphics `VkPipeline` contains the combination of state needed to perform a draw call. For every input combination (shaders, vertex layout, primitive assembly, depth testing, blending mode, etc), a new pipeline is needed. This necessitates creating and binding many pipelines for complex rendering situations. While it might appear beneficial to try to create as few pipeline as possible by increasing complexity elsewhere, it is best to profile and determine if this is truly a big performance penalty in the first place.

### Multiple queues per queue family

Several hardware platforms have more than one `VkQueue` per queue family. This can be useful by being able to submit work to the same queue family from seperate queues. While there can be advantages, it isn't necessarily better to create or use the extra queues. For performance recommendations, refer to hardware makers best practices guides.

### Descriptor Sets

Descriptor Sets are designed to group data together by their usage and update frequency. It is reasonable to have a descriptor set bound for each group of resources needed in a shader, for example object matrices, lights, textures, material information, and per-instance data. Vulkan requires hardware to be able to support at least 4 concurrently bound descriptor sets, as described by the maxBoundDescriptorSets value in `VkPhysicalDeviceLimits`, with many supporting 8 or more. Therefore is safe to use more than 1 descriptor set at a time. While there may be situations that may make a single descriptor set advantageous, refer to a best practices guide for specific details.

### Vulkan is a box of tools

In Vulkan, there are often multiple solutions to a problem. Consider passing data to a shader, one can use uniform buffers, storage buffers, vertex attributes, instance buffer, push constants, and more. Are all valid methods each with their own benefits and drawbacks. There is rarely a "perfect" solution to any problem. Therefore, use the tools available and create a good solution instead of trying to find a perfect solution.

### Correct API usage practices

While the Validation Layers can catch many types of errors, they are not perfect. Below is a short list of good habits to be in and possible sources of error when encountering odd behaviour.

* Initialize all variables and structs.
* Use the correct `sType` for each structure.
* Verify correct `pNext` chain usage, nulling it out when not needed.
* There are no default values in vulkan.
* Use correct enum, `VkFlag`, and bitmask values. 
* Considering using a type-safe Vulkan wrapper, eg [Vulkan.hpp](https://github.com/KhronosGroup/Vulkan-Hpp) for C++
* Check function return values, eg `VkResult`.
* Call clean up functions where appropriate.
