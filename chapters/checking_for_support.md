# Checking For Vulkan Support

Vulkan requires both a [Vulkan Loader](./loader.md) and a Vulkan Driver (also referred to as a _Vulkan Implementation_). The driver is in charge of translating Vulkan API calls into a valid implementation of Vulkan. The most common case is a GPU hardware vendor releasing a driver that is used to run Vulkan on a physical GPU. It should be noted that it is possible to have an entire implementation of Vulkan software based, though the performance impact would be very noticeable.

When checking for Vulkan Support it is important to distinguish the difference between _platform support_ and _device support_.

## Platform Support

The first thing to check is if your [platform](./platforms.md) even supports Vulkan. Each platform uses a different mechanism to manage how the [Vulkan Loader](./loader.md) is implemented. The loader is then in charge of determining if a Vulkan Driver is exposed correctly.

### Android

A simple way of grabbing info on Vulkan is to run the [Vulkan Hardware Capability Viewer](https://play.google.com/store/apps/details?id=de.saschawillems.vulkancapsviewer&hl=en_US) app developed by Sascha Willems. This app will not only show if Vulkan is supported, but also all the capabilities the device offers.

### Linux

Grab the [Vulkan SDK](https://vulkan.lunarg.com/sdk/home#linux) and run the [vulkaninfo](https://vulkan.lunarg.com/doc/sdk/latest/linux/vulkaninfo.html) executable to easily check for Vulkan support as well as all the capabilities the device offers.

### MacOS

Grab the [Vulkan SDK](https://vulkan.lunarg.com/sdk/home#mac) and run the [vulkaninfo](https://vulkan.lunarg.com/doc/sdk/latest/mac/vulkaninfo.html) executable to easily check for Vulkan support as well as all the capabilities the device offers.

### Windows

Grab the [Vulkan SDK](https://vulkan.lunarg.com/sdk/home#windows) and run the [vulkaninfo.exe](https://vulkan.lunarg.com/doc/sdk/latest/windows/vulkaninfo.html) executable to easily check for Vulkan support as well as all the capabilities the device offers.

## Device Support

Just because the platform supports Vulkan does not mean there is device support. For device support, one will need to make sure a Vulkan Driver is available that fully implements Vulkan. There are a few different variations of a Vulkan Driver.

### Hardware implementation

A driver targeting a physical piece of GPU hardware is the most common case for a Vulkan implementation. It is important to understand that while a certain GPU might have the physical capabilities of running Vulkan, it still requires a driver to control it. The driver is in charge of getting the Vulkan calls mapped to the hardware in the most efficient way possible.

Drivers, like any software, are updated and this means there can be many variations of drivers for the same physical device and platform. There is a [Vulkan Database](https://vulkan.gpuinfo.org/), developed and maintained by Sascha Willems, which is the largest collection of recorded Vulkan implementation details (note that just because a physical device or platform isn't in the Vulkan Database doesn't mean it couldn't exist).

### Null Driver

The term "null driver" is given to any driver that accepts Vulkan API calls, but does not do anything with them. This is common for testing interactions with the driver without needing any working implementation backing it. Many uses cases such as creating [CTS tests](./vulkan_cts.md) for new features, [testing the Validaiton Layers](https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/master/docs/creating_tests.md#running-tests-on-devsim-and-mockicd), and more rely on the idea of a null driver.

Khronos provides the [Mock ICD](https://github.com/KhronosGroup/Vulkan-Tools/tree/master/icd) as one implementation of a null driver that works on various platforms.

### Software implementation

It is possible to create a Vulkan implementation that only runs on the CPU. This is useful if there is a need to test Vulkan that is hardware independent, but unlike the null driver, also outputs a valid result.

[SwiftShader](https://github.com/google/swiftshader) is an example of CPU-based implementation.

## Ways of Checking for Vulkan

### VIA (Vulkan Installation Analyzer)

Included in the [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) is a utility to check the Vulkan installation on your computer. It is supported on Windows, Linux, and the macOS. VIA can:
 - Determine the state of Vulkan components on your system
 - Validate that your Vulkan Loader and drivers are installed properly
 - Capture your system state in a form that can be used as an attachment when submitting bugs

View the [SDK documentation on VIA](https://vulkan.lunarg.com/doc/sdk/latest/windows/via.html) for more information.

### Hello Create Instance

A simple way to check for Vulkan support cross platform is to create a simple "Hello World" Vulkan application. The `vkCreateInstance` function is used to create a Vulkan Instance and is also the shortest way to write a valid Vulkan application.

The Vulkan SDK provides a minimal [vkCreateInstance](https://vulkan.lunarg.com/doc/view/latest/windows/tutorial/html/01-init_instance.html) example `01-init_instance.cpp` that can be used.
