# VK_KHR_sampler_ycbcr_conversion

> Promoted to core in Vulkan 1.1

This extension, in short, adds support to do texture sampling on YCbCr color space natively. The Vulkan spec was originally designed only for RGB color space and therefore multiple additions to the spec were added with this extension including many new formats, the concept of multi-planar formats, image aspect plane, disjoint memory, and the `VkSamplerYcbcrConversion` object.

While this section will go over more of this extension in details, **disclaimer**:

> The use of YCbCr sampler conversion is a niche area in 3D graphics and say it's mainly used for processing inputs from video decoders and cameras. This means it is not important for the common Vulkan developer to need to understand the additions of this extension.
>
> This guide will not even attempt to teach you about YCbCr and expects you have some basic knowledge of this domain already
>
> The naming conventions and naming overload of YCbCr related concepts are quite vast. This guide will stick to `YCbCr` to mean the digital data being used as an input.
>
> For the rest of this section, the YUV420p layout will be used as an example.

## Multi-planar Formats

To represent a layout like YUV420p where all the `Y` data is in plane 0, `U` data is in plane 1, and `V` data is in plane 2 an application would use the `VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM` format. The Vulkan spec explicitly describes each multi-planar format layout and how it maps to each component. The big thing to note is all the Vulkan formats will use the `RGBA` letter notations to map to the components. For this example with YUV420p and `VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM`:

- `G` == `Y`
- `B` == `U`
- `R` == `V`

This may require some extra focus when mapping the swizzle components between `RGBA` and the YCbCr format.

## Disjoint

Normally when an application creates a `VkImage` it only binds it to a single `VkDeviceMemory` object. If the implementation supports `VK_FORMAT_FEATURE_DISJOINT_BIT` for a given format then an application can bind multiple disjoint `VkDeviceMemory` to a single `VkImage` where each `VkDeviceMemory` represents a single plane.

Doing this follows the same pattern as the normal binding of memory to an image with the use of a few new functions. Here is some pseudo code to represent the new workflow

```cpp
VkImagePlaneMemoryRequirementsInfo imagePlaneMemoryRequirementsInfo = {};
imagePlaneMemoryRequirementsInfo.planeAspect                        = VK_IMAGE_ASPECT_PLANE_0_BIT;

VkImageMemoryRequirementsInfo2 imageMemoryRequirementsInfo2 = {};
imageMemoryRequirementsInfo2.pNext                          = &imagePlaneMemoryRequirementsInfo;
imageMemoryRequirementsInfo2.image                          = myImage;

// Get memory requirement for each plane
VkMemoryRequirements2 memoryRequirements2 = {};
vkGetImageMemoryRequirements2(device, &imageMemoryRequirementsInfo2, &memoryRequirements2);

// Allocate plane 0 memory
VkMemoryAllocateInfo memoryAllocateInfo = {};
memoryAllocateInfo.allocationSize       = memoryRequirements2.memoryRequirements.size;
vkAllocateMemory(device, &memoryAllocateInfo, nullptr, &disjointMemoryPlane0));

// Allocate the same for each plane

// Bind plane 0 memory
VkBindImagePlaneMemoryInfo bindImagePlaneMemoryInfo = {};
bindImagePlaneMemoryInfo0.planeAspect               = VK_IMAGE_ASPECT_PLANE_0_BIT;

VkBindImageMemoryInfo bindImageMemoryInfo = {};
bindImageMemoryInfo.pNext        = &bindImagePlaneMemoryInfo0;
bindImageMemoryInfo.image        = myImage;
bindImageMemoryInfo.memory       = disjointMemoryPlane0;

// Bind the same for each plane

vkBindImageMemory2(device, bindImageMemoryInfoSize, bindImageMemoryInfoArray));
```

## Copying memory to each plane

Even if an application is not using disjoint memory, it still needs to use the `VK_IMAGE_ASPECT_PLANE_0_BIT` when copying over data to each plane.

For example, if an application plans to do a `vkCmdCopyBufferToImage` to copy over a single `VkBuffer` to a single non-disjoint `VkImage` the data, the logic for a YUV420p layout will look partially like

```cpp
VkBufferImageCopy bufferCopyRegions[3];
bufferCopyRegions[0].imageSubresource.aspectMask = VK_IMAGE_ASPECT_PLANE_0_BIT;
bufferCopyRegions[0].imageOffset                 = {0, 0, 0};
bufferCopyRegions[0].imageExtent.width           = myImage.width;
bufferCopyRegions[0].imageExtent.height          = myImage.height;
bufferCopyRegions[0].imageExtent.depth           = 1;

/// ...

// the U component is half the height and width
bufferCopyRegions[1].imageOffset                  = {0, 0, 0};
bufferCopyRegions[1].imageExtent.width            = myImage.width / 2;
bufferCopyRegions[1].imageExtent.height           = myImage.height / 2;
bufferCopyRegions[1].imageSubresource.aspectMask  = VK_IMAGE_ASPECT_PLANE_1_BIT;

/// ...

// the V component is half the height and width
bufferCopyRegions[2].imageOffset                  = {0, 0, 0};
bufferCopyRegions[2].imageExtent.width            = myImage.width / 2;
bufferCopyRegions[2].imageExtent.height           = myImage.height / 2;
bufferCopyRegions[2].imageSubresource.aspectMask  = VK_IMAGE_ASPECT_PLANE_2_BIT;

vkCmdCopyBufferToImage(...)
```

The big thing to note here is that the `imageOffset` is zero because its base is the plane, not the entire `VkImage`

## VkSamplerYcbcrConversion

The `VkSamplerYcbcrConversion` describes all the "read on your own outside the Vulkan Guide" aspects of YCbCr conversion. The values set here are dependent on the input YCbCr data being obtained and how to do the conversion to RGB color spacce.

Here is some pseudo code to help give an idea of how to use it from the API point of view:

```cpp
// Create conversion object that describes how to have the implementation do the YCbCr conversion
VkSamplerYcbcrConversion samplerYcbcrConversion;
VkSamplerYcbcrConversionCreateInfo samplerYcbcrConversionCreateInfo = {};
// ...
vkCreateSamplerYcbcrConversion(device, &samplerYcbcrConversionCreateInfo, nullptr, &samplerYcbcrConversion));

VkSamplerYcbcrConversionInfo samplerYcbcrConversionInfo = {};
samplerYcbcrConversionInfo.conversion                   = samplerYcbcrConversion;

// Create an ImageView with conversion
VkImageViewCreateInfo imageViewInfo = {};
imageViewInfo.pNext                 = &samplerYcbcrConversionInfo;
// ...
vkCreateImageView(device, &imageViewInfo, nullptr, &myImageView));

// Create a sampler with conversion
VkSamplerCreateInfo samplerInfo = {};
samplerInfo.pNext               = &samplerYcbcrConversionInfo;
// ...
vkCreateSampler(device, &samplerInfo, nullptr, &mySampler));
```

## combinedImageSamplerDescriptorCount

An important value to monitor is the `combinedImageSamplerDescriptorCount` which describes how many descriptor an implementation uses for each multi-planar format. This means for `VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM` an implementation can use 1, 2, or 3 descriptors for each combined image sampler used.

All descriptors in a binding use the same maximum `combinedImageSamplerDescriptorCount` descriptors to allow implementations to use a uniform stride for dynamic indexing of the descriptors in the binding.

For example, consider a descriptor set layout binding with two descriptors and immutable samplers for multi-planar formats that have `VkSamplerYcbcrConversionImageFormatProperties::combinedImageSamplerDescriptorCount` values of `2` and `3` respectively. There are two descriptors in the binding and the maximum `combinedImageSamplerDescriptorCount` is `3`, so descriptor sets with this layout consume `6` descriptors from the descriptor pool. To create a descriptor pool that allows allocating `four` descriptor sets with this layout, `descriptorCount` must be at least `24`.

Some pseudo code how to query for the `combinedImageSamplerDescriptorCount`

```cpp
VkSamplerYcbcrConversionImageFormatProperties samplerYcbcrConversionImageFormatProperties = {};

VkImageFormatProperties imageFormatProperties   = {};
VkImageFormatProperties2 imageFormatProperties2 = {};
// ...
imageFormatProperties2.pNext                    = &samplerYcbcrConversionImageFormatProperties;
imageFormatProperties2.imageFormatProperties    = imageFormatProperties;

VkPhysicalDeviceImageFormatInfo2 imageFormatInfo = {};
// ...
imageFormatInfo.format = formatToQuery;
vkGetPhysicalDeviceImageFormatProperties2(physicalDevice, &imageFormatInfo, &imageFormatProperties2));

printf("combinedImageSamplerDescriptorCount = %u\n", samplerYcbcrConversionImageFormatProperties.combinedImageSamplerDescriptorCount);
```