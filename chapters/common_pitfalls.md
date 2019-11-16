# Common Pitfalls for new Vulkan Developers

This is a short list of assumptions, traps, and anti-patterns in the Vulkan API. It is not a list of "best practices", rather it covers the common mistakes that developers new to Vulkan could easily make.

### Validation Layers

During development, ensure that the Validation Layers are enabled. They are an invaluable tool for catching mistakes while using the Vulkan API. Parameter checking, object lifetimes, and threading violations all are part of the provided error checks. A way to reassure that they are enabled is to verify if the text "Debug Messenger Added" is in the output stream. More info can be found in the [Vulkan SDK](https://vulkan.lunarg.com/doc/sdk/latest/windows/layer_configuration.html) layer documentation.

### Vulkan is a box of tools

In Vulkan, most problems can be tackled with multiple methods, each with their own benefits and drawbacks. There is rarely a "perfect" solution and obsessing over finding one is often a fruitless effort. When faced with a problem, try to create an adequate solution that meets the current needs and isn't overly convoluted. While the specification for Vulkan can be useful, it isn't the best source for how to use Vulkan in practice. Instead, reference external sources, like this guide, hardware best practice guides, tutorials, and other articles for more in-depth information. Finally, profiling various solutions is an important part of discovering which solution to use.

### Recording command buffers  

Many early Vulkan tutorials and documents recommended writing a command buffer once and re-using it wherever possible. In practice however re-use rarely has the advertized performance benefit while incurring a non-trivial development burden due to the complexity of implementation. While it may appear counterintuitive, as re-using computed data is a common optimization, managing a scene with objects being added and removed as well as techniques such as frustum culling which vary the draw calls issued on a per frame basis make reusing command buffers a serious design challenge. It requires a caching scheme to manage command buffers and maintaining state for determining if and when re-recording becomes necessary. Instead, prefer to re-record fresh command buffers every frame. If performance is a problem, recording can be multithreaded as well as using secondary command buffers for non-variable draw calls, like post processing.

### Multiple pipelines

A graphics `VkPipeline` contains the combination of state needed to perform a draw call. Rendering a scene with different shaders, blending modes, vertex layouts, etc, will require a pipeline for each possibility. Because pipeline creation and swapping them between draw calls have an associated cost, it is a good practice to create and swap pipelines only as needed. However, by using various techniques and features to further reduce creation and swapping beyond the simple cases can be counterproductive, as it adds complexity with no guarantee of benefit. For large engines this may be necessary, but otherwise it is unlikely to be a bottleneck. Using the pipeline cache can further reduce the costs without resorting to more complex schemes.

### Resource duplication per swapchain image

Pipelining frames is a common way to improve performance. By having multiple frames rendering at the same time, each using their own copy of the required resources, it reduces latency by removing resource contention. A simple implementation of this will duplicate the resources needed by each image in the swapchain. The issue is that this leads to assuming rendering resources must be duplicated once for each swapchain image. While practical for some resources, like the command buffers and semaphores used for each frame, the one to one duplication with swapchain images isn't often necessary. Vulkan offers a large amount of flexibility, letting the developer choose what level of duplication is right for their situation. Many resources may only need two copies, for example uniform buffers or data which is updated once per frame, and others may not need any duplication at all.

### Multiple queues per queue family

Several hardware platforms have more than one `VkQueue` per queue family. This can be useful by being able to submit work to the same queue family from separate queues. While there can be advantages, it isn't necessarily better to create or use the extra queues. For specific performance recommendations, refer to hardware vendors' best practices guides.

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
