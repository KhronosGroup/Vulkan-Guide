# Vulkan Guide

![Vulkan logo](./images/vulkan_logo.png)
![Khronos logo](./images/khronos_logo.png)

The Vulkan Guide is designed to help developers get up and going with the world of Vulkan. It is aimed to be a light read that leads to many other useful links depending on what a developer is looking for. All information is intended to help better fill the gaps about the many nuances of Vulkan.

## Logistics Overview
- [What is Vulkan?](./chapters/what_is_vulkan.md)
- [What you can do with Vulkan](./chapters/what_vulkan_can_do.md)
- [Vulkan Spec](./chapters/vulkan_spec.md)
- [Platforms](./chapters/platforms.md)
- [Checking for Support](./chapters/checking_for_support.md)
- [Versions](./chapters/versions.md)
    - [Vulkan Release Summary](./chapters/vulkan_release_summary.md)
- [What is SPIR-V?](./chapters/what_is_spirv.md)
- [Portability Initiative](./chapters/portability_initiative.md)
- [Vulkan CTS](./chapters/vulkan_cts.md)
- [Vulkan Development Tools](./chapters/development_tools.md)
- [Vulkan Validation Overview](./chapters/validation_overview.md)

## Using Vulkan
- [Loader](./chapters/loader.md)
- [Layers](./chapters/layers.md)
- [Querying Properties, Extensions, Features, Limits, and Formats](./chapters/querying_extensions_features.md)
    - [Enabling Extensions](./chapters/enabling_extensions.md)
    - [Enabling Features](./chapters/enabling_features.md)
- [WSI](./chapters/wsi.md)
- [pNext and sType](./chapters/pnext_and_stype.md)
- [Synchronization](./chapters/synchronization.md)
- [Memory Allocation Strategy](./chapters/memory_allocation.md)
    - [Sparse Resources](./chapters/sparse_resources.md)
- [Pipeline Caching/Derivatives](./chapters/pipeline_cache.md)
- [Threading](./chapters/threading.md)
- [Mapping Data to Shaders](./chapters/mapping_data_to_shaders.md)
- [Robustness](./chapters/robustness.md)
- [Common Pitfalls](./chapters/common_pitfalls.md)

## When and Why to use Extensions
> These are supplemental references for the various Vulkan Extensions. Please consult the Vulkan Spec for further details on any extension
- [Cleanup Extensions](./chapters/extensions/cleanup.md)
    - `VK_KHR_bind_memory2`, `VK_KHR_create_renderpass2`, `VK_KHR_dedicated_allocation`, `VK_KHR_driver_properties`, `VK_KHR_get_memory_requirements2`, `VK_KHR_get_physical_device_properties2`, `VK_EXT_host_query_reset`, `VK_KHR_maintenance1`, `VK_KHR_maintenance2`, `VK_KHR_maintenance3`, `VK_KHR_separate_depth_stencil_layouts`, `VK_EXT_separate_stencil_usage`, `VK_EXT_sampler_filter_minmax`, `VK_KHR_sampler_mirror_clamp_to_edge`
- [Device Groups](./chapters/extensions/device_groups.md)
    - `VK_KHR_device_group`, `VK_KHR_device_group_creation`
- [External Memory and Sychronization](./chapters/extensions/external.md)
    - `VK_KHR_external_fence`, `VK_KHR_external_memory`, `VK_KHR_external_semaphore`
- [Shader Features](./chapters/extensions/shader_features.md)
    - `VK_KHR_8bit_storage`, `VK_KHR_16bit_storage`, `VK_KHR_relaxed_block_layout`, `VK_KHR_shader_atomic_int64`, `VK_EXT_scalar_block_layout`, `VK_KHR_shader_clock`, `VK_EXT_shader_demote_to_helper_invocation`, `VK_KHR_shader_draw_parameters`, `VK_KHR_shader_float16_int8`, `VK_KHR_shader_float_controls`, `VK_EXT_shader_stencil_export`, `VK_EXT_shader_subgroup_ballot`, `VK_KHR_shader_subgroup_extended_types`, `VK_EXT_shader_subgroup_vote`, `VK_EXT_shader_viewport_index_layer`, `VK_KHR_spirv_1_4`, `VK_KHR_storage_buffer_storage_class`, `VK_EXT_subgroup_size_control`, `VK_KHR_uniform_buffer_standard_layout`, `VK_KHR_variable_pointers`, `VK_KHR_vulkan_memory_model`
- [Translation Layer Extensions](./chapters/extensions/translation_layer_extensions.md)
    - `VK_EXT_transform_feedback`
- [VK_EXT_descriptor_indexing](./chapters/extensions/VK_EXT_descriptor_indexing.md)
- [VK_EXT_inline_uniform_block](./chapters/extensions/VK_EXT_inline_uniform_block.md)
- [VK_EXT_memory_priority](./chapters/extensions/VK_EXT_memory_priority.md)
- [VK_KHR_descriptor_update_template](./chapters/extensions/VK_KHR_descriptor_update_template.md)
- [VK_KHR_draw_indirect_count](./chapters/extensions/VK_KHR_draw_indirect_count.md)
- [VK_KHR_image_format_list](./chapters/extensions/VK_KHR_image_format_list.md)
- [VK_KHR_imageless_framebuffer](./chapters/extensions/VK_KHR_imageless_framebuffer.md)
- [VK_KHR_sampler_ycbcr_conversion](./chapters/extensions/VK_KHR_sampler_ycbcr_conversion.md)
- [VK_KHR_timeline_semaphore](https://www.khronos.org/blog/vulkan-timeline-semaphores)
----

#### [Contributing](./CONTRIBUTING.md)
#### [License](./LICENSE)
#### [Code of conduct](./CODE_OF_CONDUCT.md)