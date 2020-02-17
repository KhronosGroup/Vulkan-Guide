# VK_KHR_buffer_device_address

> Promoted in Vulkan 1.2
>
> Formerly VK_EXT_buffer_device_address
>
> [SPV_KHR_physical_storage_buffer](https://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_physical_storage_buffer.html)
>
> [GLSL - GL_EXT_buffer_reference](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_buffer_reference.txt), [GLSL - GL_EXT_buffer_reference2](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_buffer_reference2.txt), and [GLSL - GL_EXT_buffer_reference_uvec2](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GLSL_EXT_buffer_reference_uvec2.txt)
>
> Note for people creating tools or autogenerating from the registry, the `vkGetBufferDeviceAddress` does not return `VkResult` or `void` like most API calls

This extension can be summarized as "adding pointers in shaders". It adds a new `PhysicalStorageBuffer64` addressing mode in SPIR-V and a way to query a 64-bit buffer device address via the new SPIR-V `PhysicalStorageBuffer` storage class. By calling `vkGetBufferDeviceAddress` with the `VkBuffer` to query it will return a `VkDeviceAddress` object which represents the device buffer address value. With GPUs hitting over 4GB of device memory this extension becomes important for use cases where 32-bit address space is not big enough.

There are examples of usage in the `GL_EXT_buffer_reference` spec for how to use this in a high-level shading language such as GLSL. The `GL_EXT_buffer_reference2` and `GL_EXT_buffer_reference_uvec2` extensions were added to help cover a few edge cases missed by the original `GL_EXT_buffer_reference`.

## Tracing and Capturing

This extension also allows the ability for trace capture and reply tools to use the addresses for more advance tooling purposes. These hooks to device memory for tooling are labeled as `opaqueCaptureAddress`. This is "the sharpest of razors to control the hardware" and is only designed for things such as tooling and is **highly recommended** to not attempt to use these to ship production applications.