# Portability Initiative

> **NOTICE:** Currently a provisional [VK_KHR_portability_subset](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_portability_subset.html) extension specification is available with the [vulkan_beta.h](https://github.com/KhronosGroup/Vulkan-Headers/blob/master/include/vulkan/vulkan_beta.h) headers. More information can found in the [press release](https://www.khronos.org/blog/fighting-fragmentation-vulkan-portability-extension-released-implementations-shipping).

The [Vulkan Portability Initiative](https://www.khronos.org/vulkan/portability-initiative) is an effort inside the Khronos Group to develop resources to define and evolve the [subset](https://github.com/KhronosGroup/Vulkan-Portability) of Vulkan capabilities that can be made universally available at native performance levels across all major platforms, including those not currently served by Vulkan native drivers. In a nutshell, this initiative is about making Vulkan viable on platforms that do not natively support the API (e.g MacOS and iOS).

![portability_initiative_overview.png](../images/portability_initiative_overview.png)

## Translation Layer

Layered implementations fight industry fragmentation by enabling more applications to run on more platforms, even in a fragmented industry API landscape.  For example, the first row in the diagram below shows how Vulkan is being used as a porting target to bring additional APIs to platforms to enable more content without the need for additional kernel-level drivers.  Layered API implementations have been used to successfully ship production applications on multiple platforms.

The columns in the figure show layering projects being used to make APIs available across additional platforms, even if no native drivers are available, giving application developers the deployment flexibility they need to develop with the graphics API of their choice and ship across multiple platforms.  The first colun in diagram is the work of the Vulkan Portability Initiative, enabling layered implementations of Vulkan functionality across diverse platforms.

![portability_initiative_table.png](../images/portability_initiative_table.png)

## MacOS and iOS Tools

Khronos Blog for [information about macOS and iOS support](https://www.khronos.org/blog/new-release-of-vulkan-sdk)

![portability_initiative_macos.png](../images/portability_initiative_macos.png)

## gfx-rs

Mozilla is currently helping drive [gfx-rs portability](https://github.com/gfx-rs/portability) to use [gfx-hal](https://gfx-rs.github.io/2017/07/24/low-level.html) as a way to interface with various other APIs.

![portability_initiative_gfxrs.png](../images/portability_initiative_gfxrs.png)


