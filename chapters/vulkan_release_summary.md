# Vulkan Release Summary

Each minor release of version of Vulkan has added many extensions. The Vulkan Guide has added a summary of why each extension was added and some details about the use cases. This list is taken from the Vulkan spec, but links jump to the various spots in the Vulkan Guide

# Vulkan 1.1

> [Vulkan Spec Section](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#versions-1.1)

Vulkan 1.1 was released on March 7, 2018

Besides the listed extensions below, Vulkan 1.1 introduced the [subgroups](./extensions/shader_features.md#vk-ext-shader-subgroup-ballot-and-vk-ext-shader-subgroup-vote), protected memory, and the ability to query the instance version.

- [VK_KHR_16bit_storage](./extensions/shader_features.md#vk-khr-8bit-storage-and-vk-khr-16bit-storage)
- [VK_KHR_bind_memory2](./extensions/cleanup.md#pnext-expansion)
- [VK_KHR_dedicated_allocation](./extensions/cleanup.md#vk-khr-dedicated-allocation)
- [VK_KHR_descriptor_update_template](./extensions/VK_KHR_descriptor_update_template.md)
- [VK_KHR_device_group](./extensions/device_groups.md)
- [VK_KHR_device_group_creation](./extensions/device_groups.md)
- [VK_KHR_external_fence](./extensions/external.md)
- [VK_KHR_external_fence_capabilities](./extensions/external.md)
- [VK_KHR_external_memory](./extensions/external.md)
- [VK_KHR_external_memory_capabilities](./extensions/external.md)
- [VK_KHR_external_semaphore](./extensions/external.md)
- [VK_KHR_external_semaphore_capabilities](./extensions/external.md)
- [VK_KHR_get_memory_requirements2](./extensions/cleanup.md#pnext-expansion)
- [VK_KHR_get_physical_device_properties2](./extensions/cleanup.md#pnext-expansion)
- [VK_KHR_maintenance1](./extensions/cleanup.md#maintenance-extensions)
- [VK_KHR_maintenance2](./extensions/cleanup.md#maintenance-extensions)
- [VK_KHR_maintenance3](./extensions/cleanup.md#maintenance-extensions)
- [VK_KHR_multiview](./extensions/VK_KHR_multiview.md)
- [VK_KHR_relaxed_block_layout](./extensions/shader_features.md#vk-khr-relaxed-block-layout)
- [VK_KHR_sampler_ycbcr_conversion](./extensions/VK_KHR_sampler_ycbcr_conversion.md)
- [VK_KHR_shader_draw_parameters](./extensions/shader_features.md#vk-khr-shader-draw-parameters)
- [VK_KHR_storage_buffer_storage_class](./extensions/shader_features.md#vk-khr-storage-buffer-storage-class)
- [VK_KHR_variable_pointers](./extensions/shader_features.md#vk-khr-variable-pointers)

# Vulkan 1.2

> [Vulkan Spec Section](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#versions-1.2)

Vulkan 1.2 was released on January 15, 2020

- [VK_KHR_8bit_storage](./extensions/shader_features.md#vk-khr-8bit-storage-and-vk-khr-16bit-storage)
- [VK_KHR_buffer_device_address](./extensions/VK_KHR_buffer_device_address.md)
- [VK_KHR_create_renderpass2](./extensions/cleanup.md#pnext-expansion)
- [VK_KHR_depth_stencil_resolve](./extensions/VK_KHR_depth_stencil_resolve.md)
- [VK_KHR_draw_indirect_count](./extensions/VK_KHR_draw_indirect_count.md)
- [VK_KHR_driver_properties](./extensions/cleanup.md#vk-khr-driver-properties)
- [VK_KHR_image_format_list](./extensions/image_creation.md#vk-khr-image-format-list)
- [VK_KHR_imageless_framebuffer](./extensions/VK_KHR_imageless_framebuffer.md)
- [VK_KHR_sampler_mirror_clamp_to_edge](./extensions/cleanup.md#vk-khr-sampler-mirror-clamp-to-edge)
- [VK_KHR_separate_depth_stencil_layouts](./extensions/cleanup.md#vk-khr-separate-depth-stencil-layouts)
- [VK_KHR_shader_atomic_int64](./extensions/shader_features.md#vk-khr-shader-atomic-int64)
- [VK_KHR_shader_float16_int8](./extensions/shader_features.md#vk-khr-shader-float16-int8)
- [VK_KHR_shader_float_controls](./extensions/shader_features.md#vk-khr-shader-float-controls)
- [VK_KHR_shader_subgroup_extended_types](./extensions/shader_features.md#vk-khr-shader-subgroup-extended-types)
- [VK_KHR_spirv_1_4](./extensions/shader_features.md#vk-khr-spirv-1-4)
- [VK_KHR_timeline_semaphore](https://www.khronos.org/blog/vulkan-timeline-semaphores)
- [VK_KHR_uniform_buffer_standard_layout](./extensions/shader_features.md#vk-khr-uniform-buffer-standard-layout)
- [VK_KHR_vulkan_memory_model](./extensions/shader_features.md#vk-khr-vulkan-memory-model)
- [VK_EXT_descriptor_indexing](./extensions/VK_EXT_descriptor_indexing.md)
- [VK_EXT_host_query_reset](./extensions/cleanup.md#vk-ext-host-query-reset)
- [VK_EXT_sampler_filter_minmax](./extensions/cleanup.md#vk-ext-sampler-filter-minmax)
- [VK_EXT_scalar_block_layout](./extensions/shader_features.md#vk-ext-scalar-block-layout)
- [VK_EXT_separate_stencil_usage](./extensions/image_creation.md#vk-ext-separate-stencil-usage)
- [VK_EXT_shader_viewport_index_layer](./extensions/shader_features.md#vk-ext-shader-viewport-index-layer)