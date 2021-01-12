# VK_KHR_sampler_ycbcr_conversion

> Promoted to core in Vulkan 1.1

All the examples below use a `4:2:0` multi-planar Y′C<sub>B</sub>C<sub>R</sub> format for illustration purposes.

## Multi-planar Formats

To represent a Y′C<sub>B</sub>C<sub>R</sub> image for which the Y′ (luma) data is stored in plane 0, the C<sub>B</sub> blue chroma difference value ("U") data is stored in plane 1, and the C<sub>R</sub> red chroma difference value ("V") data is stored in plane 2, an application would use the `VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM format`.

The Vulkan specification separately describes each multi-planar format representation and its mapping to each color component. Because the mapping and color conversion is separated from the format, Vulkan uses "RGB" color channel notations in the formats, and the conversion then describes the mapping from these channels to the input to the color conversion.

This allows, for example, `VK_FORMAT_B8G8R8_UNORM` images to represent Y′C<sub>B</sub>C<sub>R</sub> texels.

* `G` == `Y`
* `B` == `Cb`
* `R` == `Cr`

This may require some extra focus when mapping the swizzle components between `RGBA` and the Y′C<sub>B</sub>C<sub>R</sub> format.

## Disjoint

Normally when an application creates a `VkImage` it only binds it to a single `VkDeviceMemory` object. If the implementation supports `VK_FORMAT_FEATURE_DISJOINT_BIT` for a given format then an application can bind multiple disjoint `VkDeviceMemory` to a single `VkImage` where each `VkDeviceMemory` represents a single plane.

Image processing operations on Y′C<sub>B</sub>C<sub>R</sub> images often treat channels separately. For example, applying a sharpening operation to the luma channel or selectively denoising luma. Separating the planes allows them to be processed separately or to reuse unchanged plane data for different final images.

Using disjoint images follows the same pattern as the normal binding of memory to an image with the use of a few new functions. Here is some pseudo code to represent the new workflow:

```cpp
VkImagePlaneMemoryRequirementsInfo imagePlaneMemoryRequirementsInfo = {};
imagePlaneMemoryRequirementsInfo.planeAspect = VK_IMAGE_ASPECT_PLANE_0_BIT;

VkImageMemoryRequirementsInfo2 imageMemoryRequirementsInfo2 = {};
imageMemoryRequirementsInfo2.pNext = &imagePlaneMemoryRequirementsInfo;
imageMemoryRequirementsInfo2.image = myImage;

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

For example, if an application plans to do a `vkCmdCopyBufferToImage` to copy over a single `VkBuffer` to a single non-disjoint `VkImage` the data, the logic for a `YUV420p` layout will look partially like:

```cpp
VkBufferImageCopy bufferCopyRegions[3];
bufferCopyRegions[0].imageSubresource.aspectMask = VK_IMAGE_ASPECT_PLANE_0_BIT;
bufferCopyRegions[0].imageOffset                 = {0, 0, 0};
bufferCopyRegions[0].imageExtent.width           = myImage.width;
bufferCopyRegions[0].imageExtent.height          = myImage.height;
bufferCopyRegions[0].imageExtent.depth           = 1;

/// ...

// the Cb component is half the height and width
bufferCopyRegions[1].imageOffset                  = {0, 0, 0};
bufferCopyRegions[1].imageExtent.width            = myImage.width / 2;
bufferCopyRegions[1].imageExtent.height           = myImage.height / 2;
bufferCopyRegions[1].imageSubresource.aspectMask  = VK_IMAGE_ASPECT_PLANE_1_BIT;

/// ...

// the Cr component is half the height and width
bufferCopyRegions[2].imageOffset                  = {0, 0, 0};
bufferCopyRegions[2].imageExtent.width            = myImage.width / 2;
bufferCopyRegions[2].imageExtent.height           = myImage.height / 2;
bufferCopyRegions[2].imageSubresource.aspectMask  = VK_IMAGE_ASPECT_PLANE_2_BIT;

vkCmdCopyBufferToImage(...)
```

It is worth noting here is that the `imageOffset` is zero because its base is the plane, not the entire sname:VkImage. So when using the `imageOffset` make sure to start from base of the plane and not always plane 0.

## VkSamplerYcbcrConversion

The `VkSamplerYcbcrConversion` describes all the "out of scope explaining here" aspects of Y′C<sub>B</sub>C<sub>R</sub> conversion which are described in the https://www.khronos.org/registry/DataFormat/specs/1.3/dataformat.1.3.html#_introduction_to_color_conversions[`Khronos Data Format Specification`]. The values set here are dependent on the input Y′C<sub>B</sub>C<sub>R</sub> data being obtained and how to do the conversion to RGB color spacce.

Here is some pseudo code to help give an idea of how to use it from the API point of view:

```cpp
// Create conversion object that describes how to have the implementation do the Y′C<sub>B</sub>C<sub>R</sub> conversion
VkSamplerYcbcrConversion samplerYcbcrConversion;
VkSamplerYcbcrConversionCreateInfo samplerYcbcrConversionCreateInfo = {};
// ...
vkCreateSamplerYcbcrConversion(device, &samplerYcbcrConversionCreateInfo, nullptr, &samplerYcbcrConversion));

VkSamplerYcbcrConversionInfo samplerYcbcrConversionInfo = {};
samplerYcbcrConversionInfo.conversion = samplerYcbcrConversion;

// Create an ImageView with conversion
VkImageViewCreateInfo imageViewInfo = {};
imageViewInfo.pNext = &samplerYcbcrConversionInfo;
// ...
vkCreateImageView(device, &imageViewInfo, nullptr, &myImageView));

// Create a sampler with conversion
VkSamplerCreateInfo samplerInfo = {};
samplerInfo.pNext = &samplerYcbcrConversionInfo;
// ...
vkCreateSampler(device, &samplerInfo, nullptr, &mySampler));
```

## combinedImageSamplerDescriptorCount

An important value to monitor is the `combinedImageSamplerDescriptorCount` which describes how many descriptor an implementation uses for each multi-planar format. This means for `VK_FORMAT_G8_B8_R8_3PLANE_420_UNORM` an implementation can use 1, 2, or 3 descriptors for each combined image sampler used.

All descriptors in a binding use the same maximum `combinedImageSamplerDescriptorCount` descriptors to allow implementations to use a uniform stride for dynamic indexing of the descriptors in the binding.

For example, consider a descriptor set layout binding with two descriptors and immutable samplers for multi-planar formats that have `VkSamplerYcbcrConversionImageFormatProperties::combinedImageSamplerDescriptorCount` values of `2` and `3` respectively. There are two descriptors in the binding and the maximum `combinedImageSamplerDescriptorCount` is `3`, so descriptor sets with this layout consume `6` descriptors from the descriptor pool. To create a descriptor pool that allows allocating `4` descriptor sets with this layout, `descriptorCount` must be at least `24`.

Some pseudo code how to query for the `combinedImageSamplerDescriptorCount`:

```cpp
VkSamplerYcbcrConversionImageFormatProperties samplerYcbcrConversionImageFormatProperties = {};

VkImageFormatProperties imageFormatProperties   = {};
VkImageFormatProperties2 imageFormatProperties2 = {};
// ...
imageFormatProperties2.pNext                 = &samplerYcbcrConversionImageFormatProperties;
imageFormatProperties2.imageFormatProperties = imageFormatProperties;

VkPhysicalDeviceImageFormatInfo2 imageFormatInfo = {};
// ...
imageFormatInfo.format = formatToQuery;
vkGetPhysicalDeviceImageFormatProperties2(physicalDevice, &imageFormatInfo, &imageFormatProperties2));

printf("combinedImageSamplerDescriptorCount = %u\n", samplerYcbcrConversionImageFormatProperties.combinedImageSamplerDescriptorCount);
```
