# Vulkan Specification

The Vulkan Specification (usually referred to as the _Vulkan Spec_) is the official description of how the Vulkan API works and is ultimately used to decide what is and is not valid Vulkan usage. At first glance, the Vulkan Spec seems like an incredibly huge and dry chunk of text, but it is usually the most useful item to have open when developing.

> Reference the Vulkan Spec early and often.

## Vulkan Spec Variations

The Vulkan Spec can be built for any version and with any permutation of extensions. The Khronos Group hosts the [Vulkan Spec Registry](https://www.khronos.org/registry/vulkan/specs/) which contains a few publicly available variations that most developers will find sufficient. Anyone can build their own variation of the Vulkan Spec from [Vulkan-Docs](https://github.com/KhronosGroup/Vulkan-Docs/blob/master/BUILD.adoc).

When building the Vulkan Spec, you pass in what version of Vulkan to build for as well as what extensions to include. A Vulkan Spec without any extensions is also referred to as the [core version](https://www.khronos.org/registry/vulkan/specs/1.2/html/vkspec.html#extendingvulkan-coreversions) as it is the minimal amount of Vulkan an implementation needs to support in order to be [conformant](./vulkan_cts.md).

## Vulkan Spec Format

The Vulkan Spec can be built into different formats.

### HTML Chunked

Due to the size of the Vulkan Spec, a chunked version is the default when you visit the default `index.html` page.

Example: [https://www.khronos.org/registry/vulkan/specs/1.2/html/](https://www.khronos.org/registry/vulkan/specs/1.2/html/)

Prebuilt HTML Chunked Vulkan Spec
- The Vulkan SDK comes packaged with the chunked version of the spec. Each Vulkan SDK version includes the corresponding spec version. See the [Chunked Specification](https://vulkan.lunarg.com/doc/sdk/latest/windows/chunked_spec/index.html) for the latest Vulkan SDK.
- Vulkan 1.0 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.0/html/)
    - [Core with Extensions](https://www.khronos.org/registry/vulkan/specs/1.0-extensions/html/)
    - [Core with WSI Extensions](https://www.khronos.org/registry/vulkan/specs/1.0-wsi_extensions/html/)
- Vulkan 1.1 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.1/html/)
    - [Core with Extensions](https://www.khronos.org/registry/vulkan/specs/1.1-extensions/html/)
    - [Core with KHR Extensions](https://www.khronos.org/registry/vulkan/specs/1.1-khr-extensions/html/)
- Vulkan 1.2 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.2/html/)
    - [Core with Extensions](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/)
    - [Core with KHR Extensions](https://www.khronos.org/registry/vulkan/specs/1.2-khr-extensions/html/)

### HTML Full

If you want to view the Vulkan Spec in its entirety as HTML, you just need to view the `vkspec.html` file.

Example: https://www.khronos.org/registry/vulkan/specs/1.2/html/vkspec.html

Prebuilt HTML Full Vulkan Spec
- The Vulkan SDK comes packaged with Vulkan Spec in its entirety as HTML for the version corresponding to the Vulkan SDK version. See the [HTML version of the Specification](https://vulkan.lunarg.com/doc/sdk/latest/windows/vkspec.html) for the latest Vulkan SDK. (Note: Slow to load. The advantage of the full HTML version is its searching capability).
- Vulkan 1.0 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.0/html/vkspec.html)
    - [Core with Extensions ](https://www.khronos.org/registry/vulkan/specs/1.0-extensions/html/vkspec.html)
    - [Core with WSI Extensions](https://www.khronos.org/registry/vulkan/specs/1.0-wsi_extensions/html/vkspec.html)
- Vulkan 1.1 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.1/html/vkspec.html)
    - [Core with Extensions](https://www.khronos.org/registry/vulkan/specs/1.1-extensions/html/vkspec.html)
    - [Core with KHR Extensions](https://www.khronos.org/registry/vulkan/specs/1.1-khr-extensions/html/vkspec.html)
- Vulkan 1.2 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.2/html/vkspec.html)
    - [Core with Extensions](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html)
    - [Core with KHR Extensions](https://www.khronos.org/registry/vulkan/specs/1.2-khr-extensions/html/vkspec.html)

### PDF

To view the PDF format, visit the `pdf/vkspec.pdf` file.

Example: https://www.khronos.org/registry/vulkan/specs/1.2/pdf/vkspec.pdf

Prebuilt PDF Vulkan Spec
- Vulkan 1.0 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.0/pdf/vkspec.pdf)
    - [Core with Extensions ](https://www.khronos.org/registry/vulkan/specs/1.0-extensions/pdf/vkspec.pdf)
    - [Core with WSI Extensions](https://www.khronos.org/registry/vulkan/specs/1.0-wsi_extensions/pdf/vkspec.pdf)
- Vulkan 1.1 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.1/pdf/vkspec.pdf)
    - [Core with Extensions](https://www.khronos.org/registry/vulkan/specs/1.1-extensions/pdf/vkspec.pdf)
    - [Core with KHR Extensions](https://www.khronos.org/registry/vulkan/specs/1.1-khr-extensions/pdf/vkspec.pdf)
- Vulkan 1.2 Specification
    - [Core](https://www.khronos.org/registry/vulkan/specs/1.2/pdf/vkspec.pdf)
    - [Core with Extensions](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/pdf/vkspec.pdf)
    - [Core with KHR Extensions](https://www.khronos.org/registry/vulkan/specs/1.2-khr-extensions/pdf/vkspec.pdf)

### Man pages

The Khronos Group currently only host the Vulkan Man Pages for the latest version of the 1.2 spec, with all extensions, on the [online registry](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/).

The Vulkan Man Pages can also be found in the VulkanSDK for each SDK version. See the [Man Pages](https://vulkan.lunarg.com/doc/sdk/latest/windows/apispec.html) for the latest Vulkan SDK.
