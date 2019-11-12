# Common Pitfalls for new Vulkan Developers

This is a short list of common assumptions and traps developers new to Vulkan can make. 

### Validation Layers

During development, ensure that the Validation Layers are enabled. They are an invaluable tool for catching mistakes while using the Vulkan API. Parameter checking, object lifetimes, and threading violations all are part of the provided error checks. A way to reassure that they are enabled is to verify if the text "Debug Messenger Added" is in the output stream. More info can be found in the [Vulkan SDK](https://vulkan.lunarg.com/doc/sdk/latest/windows/layer_configuration.html) layer documentation.

### Vulkan is a box of tools

In Vulkan, most problems can be tackled with multiple methods, each with their own benefits and drawbacks. There is rarely a "perfect" solution and obsessing over finding one is often a fruitless effort. When faced with a decision, make an informed choice and create an adequate solution that meets the current needs. To become informed, use this guide, reference a hardware vendors best practices guide, and profile various solutions.  

### Recording command buffers  

Many early Vulkan tutorials and documents recommended writing a command buffer once and re-using it wherever possible. However, in practice re-use rarely has a performance benefit and incurs a non-trivial development burden. While it may appear counterintuitive, as re-using computed data is a common optimization, managing a scene with objects being added and removed as well as techniques such as frustum culling which vary draw calls on a per frame basis make reusing command buffers a serious design challenge. Instead prefer to simply re-record fresh command buffers every frame.  

### Multiple pipelines

A graphics `VkPipeline` contains the combination of state needed to perform a draw call. For every input combination (shaders, vertex layout, primitive assembly, depth testing, blending mode, etc), a new pipeline is needed. This necessitates creating and binding many pipelines for complex rendering situations. While it might appear beneficial to try to create as few pipelines as possible by increasing complexity elsewhere, it is best to profile and determine if this is truly a big performance penalty in the first place.

### Resource duplication per swapchain image

A common technique to increase throughput is to make multiple instances of a resource, where each instance can be used while rendering a different frame. The swapchain is one such example, as it contains multiple images. This can lead to the assumption that the number of instances each resource has should be the same as the swapchain image count. The issue with this assumption is that very few resources need to be duplicated the same amount as the swapchain image count. While it is useful for some things, for example the number of semaphores used to signal when a swapchain image is available, it is worth understanding which resources have one to one relationships and which don't.

### Multiple queues per queue family

Several hardware platforms have more than one `VkQueue` per queue family. This can be useful by being able to submit work to the same queue family from separate queues. While there can be advantages, it isn't necessarily better to create or use the extra queues. For performance recommendations, refer to hardware makers best practices guides.

### Descriptor Sets

Descriptor Sets are designed to facilitate grouping data used in shaders by usage and update frequency. The Vulkan Spec mandates that hardware supports using at least 4 Descriptor Sets at a time, with most hardware supporting at least 8. Therefore there is very little reason not to use more than one where it is sensible.

### Correct API usage practices

While the Validation Layers can catch many types of errors, they are not perfect. Below is a short list of good habits and possible sources of error when encountering odd behavior.

* Initialize all variables and structs.
* Use the correct `sType` for each structure.
* Verify correct `pNext` chain usage, nulling it out when not needed.
* There are no default values in Vulkan.
* Use correct enum, `VkFlag`, and bitmask values. 
* Consider using a type-safe Vulkan wrapper, eg. [Vulkan.hpp](https://github.com/KhronosGroup/Vulkan-Hpp) for C++
* Check function return values, eg `VkResult`.
* Call cleanup functions where appropriate.
