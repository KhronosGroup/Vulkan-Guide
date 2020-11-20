# Vulkan Validation Overview

> The purpose of this section is to give a full overview of how Vulkan deals with __valid usage__ of the API.

## Valid Usage (VU)

A **VU** is explicitly [defined in the Vulkan Spec](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#fundamentals-validusage) as:

> set of conditions that **must** be met in order to achieve well-defined run-time behavior in an application.

One of the main advantages of Vulkan, as an explicit API, is that the implementation (driver) doesn't waste time checking for valid input. In OpenGL, the implementation would have to always check for valid usage which added noticeable overhead. There is no [glGetError](https://www.khronos.org/opengl/wiki/OpenGL_Error) equivalent in Vulkan.

The valid usages will be listed in the spec after every function and structure. For example, if a VUID checks for an invalid `VkImage` at `VkBindImageMemory` then the valid usage in the spec is found under `VkBindImageMemory`. This is because the Validation Layers will only know about all the information at `VkBindImageMemory` during the execution of the application.

## Undefined Behavior

When an application supplies invalid input, according to the valid usages in the spec, the result is __undefined behavior__. In this state, Vulkan makes no guarantees as [anything is possible with undefined behavior](https://raphlinus.github.io/programming/rust/2018/08/17/undefined-behavior.html).

**VERY IMPORTANT**: While undefined behavior might seem to work on one implementation, there is a good chance it will fail on another.

## Valid Usage ID (VUID)

A `VUID` is an unique ID given to each valid usage. This allows a way to point to a valid usage in the spec easily.

Using `VUID-vkBindImageMemory-memoryOffset-01046` as an example, it is as simple as adding the VUID to an anchor in the HMTL version of the spec ([vkspec.html#VUID-vkBindImageMemory-memoryOffset-01046](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VUID-vkBindImageMemory-memoryOffset-01046)) and it will jump right to the VUID.

## Khronos Validation Layer

Since Vulkan doesn't do any error checking, it is **very important**, when developing, to enable the [Validation Layers](https://github.com/KhronosGroup/Vulkan-ValidationLayers) right away to help catch invalid behavior. Applications should also never ship the Validation Layers with their application as they noticeably reduce performance and are designed for the development phase.

> The Khronos Validation Layer used to consist of multiple layers but now has been unified to a single `VK_LAYER_KHRONOS_validition` layer. [More details explained in LunarG's whitepaper](https://www.lunarg.com/wp-content/uploads/2019/04/UberLayer_V3.pdf).

### Getting Validation Layers

The Validation Layers are constantly being updated and improved so it is always possible to grab the source and [build it yourself](https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/master/BUILD.md). In case you want a prebuit version there are various options for all supported platforms:

- **Android** - Binaries are [released on GitHub](https://github.com/KhronosGroup/Vulkan-ValidationLayers/releases) with most up to date version. The NDK will also comes with the Validation Layers built and [information on how to use them](https://developer.android.com/ndk/guides/graphics/validation-layer).
- **Linux** - The [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) comes with the Validation Layers built and instructions on how to use them on [Linux](https://vulkan.lunarg.com/doc/sdk/latest/linux/validation_layers.html).
- **MacOS** - The [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) comes with the Validation Layers built and instructions on how to use them on [MacOS](https://vulkan.lunarg.com/doc/sdk/latest/mac/validation_layers.html).
- **Windows** - The [Vulkan SDK](https://vulkan.lunarg.com/sdk/home) comes with the Validation Layers built and instructions on how to use them on [Windows](https://vulkan.lunarg.com/doc/sdk/latest/windows/validation_layers.html).

## Breaking Down a Validation Error Message

The Validation Layers attempt to supply as much useful information as possible when an error occurs. The following examples are to help show how to get the most information out of the Validation Layers

- Example 1 - Implicit Valid Usage
    - This example shows a case where an [implicit VU](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#fundamentals-implicit-validity) is triggered. There will not be a number at the end of the VUID.
    ```
    Validation Error: [ VUID-vkBindBufferMemory-memory-parameter ] Object 0: handle =
    0x20c8650, type = VK_OBJECT_TYPE_INSTANCE; | MessageID = 0xe9199965 | Invalid
    VkDeviceMemory Object 0x60000000006. The Vulkan spec states: memory must be a valid
    VkDeviceMemory handle (https://www.khronos.org/registry/vulkan/specs/1.1-extensions/
    html/vkspec.html#VUID-vkBindBufferMemory-memory-parameter)
    ```

    - The first thing to note is the VUID is listed first in the message (`VUID-vkBindBufferMemory-memory-parameter`)
        - There is also a link at the end of the message to the VUID in the spec
    - `The Vulkan spec states:` is the quoted VUID from the spec.
    - The `VK_OBJECT_TYPE_INSTANCE` is the [VkObjectType](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#_debugging)
    - `Invalid VkDeviceMemory Object 0x60000000006` is the [Dispatchable Handle](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#fundamentals-objectmodel-overview) to help show which `VkDeviceMemory` handle was the cause of the error.

- Example 2 - Explicit Valid Usage
    - This example shows an error where some `VkImage` is trying to be bound to 2 different `VkDeviceMemory` objects
    ```
    Validation Error: [ VUID-vkBindImageMemory-image-01044 ] Object 0: handle =
    0x90000000009, name = myTextureMemory, type = VK_OBJECT_TYPE_DEVICE_MEMORY; Object 1:
    handle = 0x70000000007, type = VK_OBJECT_TYPE_IMAGE; Object 2: handle = 0x90000000006,
    name = myIconMemory, type = VK_OBJECT_TYPE_DEVICE_MEMORY; | MessageID = 0x6f3eac96 |
    In vkBindImageMemory(), attempting to bind VkDeviceMemory 0x90000000009[myTextureMemory]
    to VkImage 0x70000000007[] which has already been bound to VkDeviceMemory
    0x90000000006[myIconMemory]. The Vulkan spec states: image must not already be
    backed by a memory object (https://www.khronos.org/registry/vulkan/specs/1.1-extensions/
    html/vkspec.html#VUID-vkBindImageMemory-image-01044)
    ```

    - Example 2 is about the same as Example 1 with the exception that the `name` that was attached to the object (`name = myTextureMemory`). This was done using the [VK_EXT_debug_util](https://www.lunarg.com/new-tutorial-for-vulkan-debug-utilities-extension/) extension ([Sample of how to use the extension](https://github.com/KhronosGroup/Vulkan-Samples/blob/master/samples/extensions/debug_utils/debug_utils_tutorial.md)). Note that the old way of using [VK_EXT_debug_report](https://www.saschawillems.de/blog/2016/05/28/tutorial-on-using-vulkans-vk_ext_debug_marker-with-renderdoc/) might be needed on legacy devices that don't support `VK_EXT_debug_util`.
    - There were 3 objects involved in causing this error.
        - Object 0 is a `VkDeviceMemory` named `myTextureMemory`
        - Object 1 is a `VkImage` with no name
        - Object 2 is a `VkDeviceMemory` named `myIconMemory`
    - With the names it is easy to see "In `vkBindImageMemory()`, the `myTextureMemory` memory was attempting to bind to an image already been bound to the `myIconMemory` memory".

Each error message contains a uniform logging pattern. This allows information to be easily found in any error. The pattern is as followed:
- Log status (ex. `Error:`, `Warning:`, etc)
- The VUID
- Array of objects involved
    - Index of array
    - Dispatch Handle value
    - Optional name
    - Object Type
- Function or struct error occurred in
- Message the layer has created to help describe the issue
- The full Valid Usage from the spec
- Link to the Valid Usage

## Multiple VUIDs

> Note: The following is not ideal and is being looked into how to make it simpler

Currently, the spec is designed to only show the VUIDs depending on the [version and extensions the spec was built with](vulkan_spec.md#vulkan-spec-variations). Simply put, additions of extensions and versions may alter the VU language enough (from new API items added) that a separate VUID is created.

An example of this from the [Vulkan-Docs](https://github.com/KhronosGroup/Vulkan-Docs) where the [spec in generated from](./vulkan_spec.md)

```
ifndef::VK_VERSION_1_2,VK_EXT_descriptor_indexing[]
  * [[VUID-VkPipelineLayoutCreateInfo-pSetLayouts-00287]]
    ...
endif::VK_VERSION_1_2,VK_EXT_descriptor_indexing[]
ifdef::VK_VERSION_1_2,VK_EXT_descriptor_indexing[]
  * [[VUID-VkPipelineLayoutCreateInfo-descriptorType-03016]]
    ...
endif::VK_VERSION_1_2,VK_EXT_descriptor_indexing[]
```

What this creates is two very similar VUIDs

In this example, both VUIDs are very similar and the only difference is the fact `VK_DESCRIPTOR_SET_LAYOUT_CREATE_UPDATE_AFTER_BIND_POOL_BIT` is referenced in one and not this other. This is because the enum was added with the addition of `VK_EXT_descriptor_indexing` which is now part of Vulkan 1.2.

This means the 2 valid [html links to the spec](./vulkan_spec.md#html-full) would look like

- `1.1/html/vkspec.html#VUID-VkPipelineLayoutCreateInfo-pSetLayouts-00287`
- `1.2/html/vkspec.html#VUID-VkPipelineLayoutCreateInfo-descriptorType-03016`

The Validation Layer uses the device properties of the application in order to decide which one to display. So in this case, if you are running on a Vulkan 1.2 implementation or a device that supports `VK_EXT_descriptor_indexing` it will display the VUID `03016`.

## Special Usage Tags

The [Best Practices layer](https://vulkan.lunarg.com/doc/sdk/latest/windows/best_practices.html) will produce warnings when an application tries to use any extension with [special usage tags](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#extendingvulkan-compatibility-specialuse). An example of such an extension is [VK_EXT_transform_feedback](extensions/translation_layer_extensions.md#vk_ext_transform_feedback) which is only designed for emulation layers. If an application's intended usage corresponds to one of the special use cases, the following approach will allow you to ignore the warnings.

Ignoring Special Usage Warnings with `VK_EXT_debug_report`

```cpp
VkBool32 DebugReportCallbackEXT(/* ... */ const char* pMessage /* ... */)
{
    // If pMessage contains "specialuse-extension", then exit
    if(strstr(pMessage, "specialuse-extension") != NULL) {
        return VK_FALSE;
    };

    // Handle remaining validation messages
}
```

Ignoring Special Usage Warnings with `VK_EXT_debug_utils`

```cpp
VkBool32 DebugUtilsMessengerCallbackEXT(/* ... */ const VkDebugUtilsMessengerCallbackDataEXT* pCallbackData /* ... */)
{
    // If pMessageIdName contains "specialuse-extension", then exit
    if(strstr(pCallbackData->pMessageIdName, "specialuse-extension") != NULL) {
        return VK_FALSE;
    };

    // Handle remaining validation messages
}
```