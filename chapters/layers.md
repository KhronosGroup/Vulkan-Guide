# Layers

Layers are optional components that augment the Vulkan system. They can intercept, evaluate, and modify existing Vulkan functions on their way from the application down to the hardware. Layer's properties can be queried from an application with [vkEnumerateInstanceLayerProperties](https://www.khronos.org/registry/vulkan/specs/1.2/html/vkspec.html#vkEnumerateInstanceLayerProperties).

## Using Layers

Layers are packaged as shared libraries that get dynamically loaded in by the loader and inserted between it and the application. The two things needed to use layers are the location of the binary files and which layers to enable. The layers to use can be either explicitly enabled by the application or implicitly enabled by telling the loader to use them. More details about implicit and explicit layers can be found in the [Loader and Layer Interface](https://github.com/KhronosGroup/Vulkan-Loader/blob/master/loader/LoaderAndLayerInterface.md#implicit-vs-explicit-layers).

The [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) contains a [layer configuration document](https://vulkan.lunarg.com/doc/sdk/latest/windows/layer_configuration.html) that is very specific to how to discover and configure layers on each of the platforms.

## Vulkan Configurator Tool
Developers on Windows, Linux, and macOS can use the Vulkan Configurator, vkconfig, to enable explicit layers and disable implicit layers as well as change layer settings from a graphical user interface.
Please see the [Vulkan Configurator documentation](https://vulkan.lunarg.com/doc/sdk/latest/windows/vkconfig.html) in the Vulkan SDK for more information on using the Vulkan Configurator.

## Device Layers Deprecation

There used to be both instance layers and device layers, but device layers were [deprecated](https://www.khronos.org/registry/vulkan/specs/1.2/html/vkspec.html#extendingvulkan-layers-devicelayerdeprecation) early in Vulkan's life and should be avoided.

## Creating a Layer

Anyone can create a layer as long as it follows the [loader to layer interface](https://github.com/KhronosGroup/Vulkan-Loader/blob/master/loader/LoaderAndLayerInterface.md#loader-and-layer-interface) which is how the loader and layers agree to communicate with each other.

The Vulkan SDK also provides a [Layer Factory](https://vulkan.lunarg.com/doc/sdk/latest/windows/layer_factory.html) framework to help develop new layers ([Video presentation](https://www.youtube.com/watch?v=gVT7nyXz6M8&t=5m22s)).
The layer factory hides the majority of the loader-layer interface, layer boilerplate, setup and initialization, and complexities of layer development.
During application development, the ability to easily create a layer to aid in debugging your application can be useful.
For more information, see the [Vulkan Layer Factory documentation](https://vulkan.lunarg.com/doc/sdk/latest/windows/layer_factory.html) in the [Vulkan SDK](https://vulkan.lunarg.com/sdk/home).

## Platform Variations

The way to load a layer in implicitly varies between loader and platform.

### Android

As of Android P (Android 9 / API level 28), if a device is in a debuggable state such that `getprop ro.debuggable` [returns 1](http://androidxref.com/9.0.0_r3/xref/frameworks/native/vulkan/libvulkan/layers_extensions.cpp#454), then the loader will look in [/data/local/debug/vulkan](http://androidxref.com/9.0.0_r3/xref/frameworks/native/vulkan/libvulkan/layers_extensions.cpp#67).

Starting in Android P (Android 9 / API level 28) implicit layers can be [pushed using ADB](https://developer.android.com/ndk/guides/graphics/validation-layer#vl-adb) if the application was built in debug mode.

There is no way other than the options above to use implicit layers.

### Linux

The [Vulkan SDK](https://vulkan.lunarg.com/doc/sdk/latest/linux/layer_configuration.html) explains how to use implicit layers on Linux.

### MacOS

The [Vulkan SDK](https://vulkan.lunarg.com/doc/sdk/latest/mac/layer_configuration.html) explains how to use implicit layers on MacOS.

### Windows

The [Vulkan SDK](https://vulkan.lunarg.com/doc/sdk/latest/windows/layer_configuration.html) explains how to use implicit layers on Windows.
