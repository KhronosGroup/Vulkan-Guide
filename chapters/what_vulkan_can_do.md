# What Vulkan Can Do

Vulkan can be used to develop applications for many use cases. While Vulkan applications can choose to use a subset of the functionality described below, it was designed so a developer could use all of them in a single API.

> Note: It is important to understand Vulkan is a box of tools and there are multiple ways of doing a task.

## Graphics

2D and 3D graphics are primarily what the Vulkan API is designed for. Vulkan is designed to allow developers to create hardware accelerated graphical applications.

> Note: All Vulkan implementations are required to support Graphics, but the [WSI](./wsi.md) system is not required.

## Compute

Due to the parallel nature of GPUs, a new style of programming referred to as [GPGPU](https://en.wikipedia.org/wiki/General-purpose_computing_on_graphics_processing_units) can be used to exploit a GPU for computational tasks. Vulkan supports compute variations of `VkQueues`, `VkPipelines`, and more which allow Vulkan to be used for general computation.

> Note: All Vulkan implementations are required to support Compute.

## Ray Tracing

Currently, the Vulkan Working Group is looking into how to make Vulkan a first class API for Ray Tracing rendering. More information was announced at [Siggraph 2019](https://www.youtube.com/watch?v=_57aiwJISCI&feature=youtu.be&t=5220).

> Note: As of now, there is an [NVIDIA vendor extension](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VK_NV_ray_tracing) exposing an implementation of ray tracing on Vulkan.

## Video

Currently, the Vulkan Working Group is looking into how to make Vulkan a first class API for exposing onboard GPUs video encode/decode support. More information was announced at [Siggraph 2019](https://www.youtube.com/watch?v=_57aiwJISCI&feature=youtu.be&t=4948).

> Note: As of now, there exists no public Vulkan API for video.

## Machine Learning

Currently, the Vulkan Working Group is looking into how to make Vulkan a first class API for exposing ML compute capabilities of modern GPUs. More information was announced at [Siggraph 2019](https://www.youtube.com/watch?v=_57aiwJISCI&feature=youtu.be&t=5007).

> Note: As of now, there exists no public Vulkan API for machine learning.

## Safety Critical

Currently, the Vulkan Working Group is looking into how to make Vulkan usable for safety critical systems.

> Note: As of now, there exists no public Vulkan API for safety critical systems.
