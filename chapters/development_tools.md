# Development Tools

The Vulkan ecosystem consists of many tools for development. This is **not** a full list and this is offered as a good starting point for many developers. Please continue to do your own research and search for other tools as the development ecosystem is much larger than what can reasonably fit on a single Markdown page.

Khronos hosts [Vulkan Samples](https://github.com/KhronosGroup/Vulkan-Samples), a collection of code and tutorials that demonstrates API usage and explains the implementation of performance best practices.

LunarG is privately sponsored to develop and maintain Vulkan ecosystem components and is currently the curator for the [Vulkan Loader](https://github.com/KhronosGroup/Vulkan-Loader) and [Vulkan Validation Layers](https://github.com/KhronosGroup/Vulkan-ValidationLayers) Khronos Group repositores. In addition, LunarG delivers the [Vulkan SDK](https://vulkan.lunarg.com/) and develops other key tools such as the [Vulkan Configurator](https://vulkan.lunarg.com/doc/sdk/latest/windows/vkconfig.html) and [GFXReconstruct](https://vulkan.lunarg.com/doc/sdk/latest/windows/capture_tools.html).

## Vulkan Layers

Layers are optional components that augment the Vulkan system. They can intercept, evaluate, and modify existing Vulkan functions on their way from the application down to the hardware. Layers are implemented as libraries that can be enabled and configured using [Vulkan Configurator](https://vulkan.lunarg.com/doc/sdk/latest/windows/vkconfig.html).

### Khronos Layers

- [`VK_LAYER_KHRONOS_validation`](./validation_overview.md#khronos-validation-layer), the Khronos Validation Layer.
It is every developer's first layer of defense when debugging their Vulkan application and this is the reason it is at the top of this list. Read the [Validation Overview chapter](./validation_overview.md) for more details.
The validation layer included multiple features:
  - [Synchronization Validation](https://vulkan.lunarg.com/doc/sdk/latest/windows/synchronization_usage.html): Identify resource access conflicts due to missing or incorrect synchronization operations between actions (Draw, Copy, Dispatch, Blit) reading or writing the same regions of memory.
  - [GPU-Assisted Validation](https://vulkan.lunarg.com/doc/sdk/latest/windows/gpu_validation.html): Instrument shader code to perform run-time checks for error conditions produced during shader execution.
  - [Shader printf](https://vulkan.lunarg.com/doc/sdk/latest/windows/debug_printf.html): Debug shader code by "printing" any values of interest to the debug callback or stdout.
  - [Best Practices Warnings](https://vulkan.lunarg.com/doc/sdk/latest/windows/best_practices.html): Highlights potential performance issues, questionable usage patterns, common mistakes.

- [`VK_LAYER_KHRONOS_synchronization2`](https://vulkan.lunarg.com/doc/view/latest/windows/synchronization2_layer.html), the Khronos Synchronization2 layer.
The `VK_LAYER_KHRONOS_synchronization2` layer implements the `VK_KHR_synchronization2` extension. By default, it will disable itself if the underlying driver provides the extension.

### Vulkan SDK layers

Besides the Khronos Layers, the Vulkan SDK included additional useful platform independent layers.

- [`VK_LAYER_LUNARG_api_dump`](https://vulkan.lunarg.com/doc/sdk/latest/windows/api_dump_layer.html), a layer to log Vulkan API calls.
The API dump layer prints API calls, parameters, and values to the identified output stream.

- [`VK_LAYER_LUNARG_gfxreconstruct`](https://vulkan.lunarg.com/doc/sdk/latest/windows/capture_tools.html), a layer for capturing frames created with Vulkan.
This layer is a part of GFXReconstruct, a software for capturing and replaying Vulkan API calls. Full Android support is also available at <https://github.com/LunarG/gfxreconstruct>

- [`VK_LAYER_LUNARG_device_simulation`](https://vulkan.lunarg.com/doc/sdk/latest/windows/device_simulation_layer.html), a layer to test Vulkan applications portability.
The device simulation layer can be used to test whether a Vulkan application would run on a Vulkan device with lower capabilities.

- [`VK_LAYER_LUNARG_screenshot`](https://vulkan.lunarg.com/doc/sdk/latest/windows/screenshot_layer.html), a screenshot layer.
Captures the rendered image of a Vulkan application to a viewable image.

- [`VK_LAYER_LUNARG_monitor`](https://vulkan.lunarg.com/doc/sdk/latest/windows/monitor_layer.html), a framerate monitor layer.
Display the Vulkan application FPS in the window title bar to give a hint about the performance.

### Vulkan Third-party layers

There are also other publicly available layers that can be used to help in development.

- [`VK_LAYER_ARM_mali_perf_doc`](https://github.com/ARM-software/perfdoc), the ARM PerfDoc layer.
Checks Vulkan applications for best practices on Arm Mali devices.

- [`VK_LAYER_IMG_powervr_perf_doc`](https://github.com/powervr-graphics/perfdoc), the PowerVR PerfDoc layer.
Checks Vulkan applications for best practices on Imagination Technologies PowerVR devices.

- [`VK_LAYER_adreno`](https://developer.qualcomm.com/software/adreno-gpu-sdk/tools), the Vulkan Adreno Layer.
Checks Vulkan applications for best practices on Qualcomm Adreno devices.

## Debugging

Debugging something running on a GPU can be incredibly hard, luckily there are tools out there to help.

- [Arm Graphics Analyzer](https://developer.arm.com/tools-and-software/graphics-and-gaming/arm-mobile-studio/components/graphics-analyzer)
- [GAPID](https://github.com/google/gapid)
- [NVIDIA Nsight](https://developer.nvidia.com/nsight-graphics)
- [PVRCarbon](https://developer.imaginationtech.com)
- [RenderDoc](https://renderdoc.org/)
- [GFXReconstruct](https://vulkan.lunarg.com/doc/sdk/latest/windows/capture_tools.html)

## Profiling

With anything related to a GPU it is best to not assume and profile when possible. Here is a list of known profilers to aid in your development.

- [AMD Radeon GPU Profiler](https://gpuopen.com/rgp/) - Low-level performance analysis tool for AMD Radeon GPUs.
- [Arm Streamline Performance Analyzer](https://developer.arm.com/tools-and-software/graphics-and-gaming/arm-mobile-studio/components/streamline-performance-analyzer) - Visualize the performance of mobile games and applications for a broad range of devices, using Arm Mobile Studio.
- [Intel(R) GPA](https://software.intel.com/content/www/us/en/develop/tools/graphics-performance-analyzers.html) - Intel's Graphics Performance Analyzers that supports capturing and analyzing multi-frame streams of Vulkan apps.
- [OCAT](https://github.com/GPUOpen-Tools/OCAT) - The Open Capture and Analytics Tool (OCAT) provides an FPS overlay and performance measurement for D3D11, D3D12, and Vulkan.
- [PVRTune](https://developer.imaginationtech.com)
- [Qualcomm Snapdragon Profiler](https://developer.qualcomm.com/software/snapdragon-profiler) - Profiling tool targeting Adreno GPU.
