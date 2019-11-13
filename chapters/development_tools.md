# Development Tools

The Vulkan ecosystem consists of many tools for development. This is **not** a full list and this is offered as a good starting point for many developers. Please continue to do your own research and searching for other tools as the development ecosystem is much larger than what can reasonably fit on a single markdown page.

Khronos hosts [Vulkan Samples](https://github.com/KhronosGroup/Vulkan-Samples), a collection of code and tutorials that demonstrate API usage and explain the implementation of performance best-practices.

## Khronos Validation Layer
Since Vulkan doesn't do any error checking, it is very important when developing to enable the [Validation Layers](https://github.com/KhronosGroup/Vulkan-ValidationLayers) right away to help to catch invalid behavior. While invalid behavior might seem to work on one implementation, there is a good chance it will fail on another. Applications should also never ship the Validation Layers with their application as they noticeably reduce performance and are designed for the development phase.

> The Khronos Validation Layer used to consist of multiple layers but now has been unified for [details explained in LunarG's whitepaper](https://www.lunarg.com/wp-content/uploads/2019/04/UberLayer_V3.pdf).

- **Android** - The NDK comes with the Validation Layers built and [information on how to use them](https://developer.android.com/ndk/guides/graphics/validation-layer).
- **Linux** - The [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) comes with the Validation Layers built and instructions on how to use them on [Linux](https://vulkan.lunarg.com/doc/sdk/latest/linux/validation_layers.html).
- **MacOS** - The [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) comes with the Validation Layers built and instructions on how to use them on [MacOS](https://vulkan.lunarg.com/doc/sdk/latest/mac/validation_layers.html).
- **Windows** - The [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) comes with the Validation Layers built and instructions on how to use them on [Windows](https://vulkan.lunarg.com/doc/sdk/latest/windows/validation_layers.html).

## Vulkan Layers

Besides the Validation Layers, there are also other publicly available layers that can be used to help in development.

- [API Logging](https://vulkan.lunarg.com/doc/sdk/latest/windows/api_dump_layer.html) - Vulkan SDK layer for logging API calls.
- [Arm PerfDoc layer](https://github.com/ARM-software/perfdoc) - Checks Vulkan applications for best practices on Arm Mali devices.
- [LunarG Best Practices layer](https://vulkan.lunarg.com/doc/sdk/latest/windows/best_practices.html) - Highlights potential performance issues, questionable usage patterns, common mistakes.
- [Simulate device properties](https://vulkan.lunarg.com/doc/sdk/latest/windows/device_simulation_layer.html) - Vulkan SDK layer for testing device properties on any device.
- [Take screenshots](https://vulkan.lunarg.com/doc/sdk/latest/windows/screenshot_layer.html) - Captures the rendered image to a viewable image.
- [Track FPS](https://vulkan.lunarg.com/doc/sdk/latest/windows/monitor_layer.html) - Logs FPS information.


## Debugging

Debugging something running on a GPU can be incredibly hard, luckly there are tools out there to help.

- [Arm Graphics Analyzer](https://developer.arm.com/tools-and-software/graphics-and-gaming/arm-mobile-studio/components/graphics-analyzer)
- [GAPID](https://github.com/google/gapid)
- [NVIDIA Nsight](https://developer.nvidia.com/nsight-graphics)
- [PVRCarbon](https://www.imgtec.com/developers/)
- [RenderDoc](https://renderdoc.org/)

## Profiling

With anything related to a GPU it is best to not assume and profile when possible. Here is a list of known profilers to aid in your development.

- [AMD Radeon GPU Profiler](https://gpuopen.com/gaming-product/radeon-gpu-profiler-rgp/) - Low-level performance analysis tool for AMD Radeon GPUs.
- [Arm Streamline Performance Analyzer](https://developer.arm.com/tools-and-software/graphics-and-gaming/arm-mobile-studio/components/streamline-performance-analyzer) - Visualize the performance of mobile games and applications for a broad range of devices, using Arm Mobile Studio.
- [OCAT](https://github.com/GPUOpen-Tools/OCAT) - The Open Capture and Analytics Tool (OCAT) provides an FPS overlay and performance measurement for D3D11, D3D12, and Vulkan.
- [PVRTune](https://www.imgtec.com/developers/)
- [Qualcomm Snapdragon Profiler](https://developer.qualcomm.com/software/snapdragon-profiler) - Profiling tool targeting Adreno GPU.
