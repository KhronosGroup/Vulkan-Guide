# Push Constants

The Vulkan spec defines `Push Constants` as:

> A small bank of values writable via the API and accessible in shaders. Push constants allow the application to set values used in shaders without creating buffers or modifying and binding descriptor sets for each update.

- [How to use](#how-to-use)
  * [Shader Code](#shader-code)
  * [Pipeline layout](#pipeline-layout)
  * [Updating at record time](#updating-at-record-time)
  * [Offsets](#offsets)
- [Pipeline layout compatibility](#pipeline-layout-compatibility)
- [Lifetime of push constants](#lifetime-of-push-constants)
  * [Binding descriptor sets has no effect](#binding-descriptor-sets-has-no-effect)
  * [Mixing bind points](#mixing-bind-points)
  * [Binding non-compatible pipelines](#binding-non-compatible-pipelines)
  * [Layouts with no static push constants](#layouts-with-no-static-push-constants)
  * [Updated incrementally](#updated-incrementally)
  * [Pushing data with non-compatible layouts](#pushing-data-with-non-compatible-layouts)
# How to use

## Shader Code

The first thing needed is a shader to match with the [push constant interface](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#interfaces-resources-pushconst). A simple GLSL fragment shader example:

```glsl
layout(push_constant, std430) uniform pc {
    vec4 data;
};
layout(location = 0) out vec4 outColor;
void main() {
   outColor = data;
}
```

Which when looking at parts of the disassembled SPIR-V

```swift
                  OpMemberDecorate %pc 0 Offset 0
                  OpDecorate %pc Block

         %float = OpTypeFloat 32
       %v4float = OpTypeVector %float 4

%pc             = OpTypeStruct %v4float
%pc_ptr         = OpTypePointer PushConstant %pc
%pc_var         = OpVariable %pc_ptr PushConstant
%pc_v4float_ptr = OpTypePointer PushConstant %v4float

%access_chain   = OpAccessChain %pc_v4float_ptr %pc_var %int_0
```

it matches the [Vulkan spec](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#interfaces-resources-pushconst) description of being typed as an `OpTypeStruct` and `Block` decorated.

## Pipeline layout

When calling `vkCreatePipelineLayout` the [push constant ranges](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VkPushConstantRange.html) needs to be set in [VkPipelineLayoutCreateInfo](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VkPipelineLayoutCreateInfo.html).

An example using the above the shader would look like:

```cpp
VkPushConstantRange range = {};
range.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
range.offset = 0;
range.size = 16; // %v4float (vec4) is defined as 16 bytes

VkPipelineLayoutCreateInfo create_info = {};
create_info.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
create_info.pNext = NULL;
create_info.flags = 0;
create_info.setLayoutCount = 0;
create_info.pushConstantRangeCount = 1;
create_info.pPushConstantRanges = &range;

VkPipelineLayout pipeline_layout;
vkCreatePipelineLayout(device, &create_info, NULL, &pipeline_layout);
```

## Updating at record time

Lastly, the value for the push constants needs to be updated to the desired value using [vkCmdPushConstants](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/vkCmdPushConstants.html). Using the above example, the following example of what this looks like:


```cpp
float data[4] = {0.0f, 1.0f, 2.0f, 3.0f}; // where sizeof(float) == 4 bytes

// vkBeginCommandBuffer(commandBuffer) called prior

vkCmdPushConstants(commandBuffer, pipeline_layout, VK_SHADER_STAGE_FRAGMENT_BIT, 0, 16, data);

// draw / dispatch / trace rays / etc
```

## Offsets

Taking the above shader, one can add an offset to the push constant block

```patch
layout(push_constant, std430) uniform pc {
-   vec4 data;
+   layout(offset = 32) vec4 data;
};
layout(location = 0) out vec4 outColor;
void main() {
   outColor = data;
}
```

The difference from the above disassembled SPIR-V is only the member decoration

```patch
- OpMemberDecorate %pc 0 Offset 0
+ OpMemberDecorate %pc 0 Offset 32
```

From here the offset of `32` needs to be also specified in `VkPushConstantRange` for each shader stage that uses it

```cpp
VkPushConstantRange range = {VK_SHADER_STAGE_FRAGMENT_BIT, 32, 16};
```

The last step is to make sure the offset is also part of the `vkCmdPushConstants` call

```cpp
vkCmdPushConstants(commandBuffer, pipeline_layout, VK_SHADER_STAGE_FRAGMENT_BIT, 32, 16, data);
```

# Pipeline layout compatibility

The Vulkan spec defines what [Compatibility for push constants](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#descriptorsets-compatibility) as

> if they were created with identical push constant ranges

This means before a [bound pipeline command is issued](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#pipeline-bindpoint-commands) (such as `vkCmdDraw`) the `VkPipelineLayout` used in the last `vkCmdPushConstants` and `vkCmdBindPipeline` (for the appropriate `VkPipelineBindPoint`) must have had identical `VkPushConstantRange`.

# Lifetime of push constants

The lifetime of push constants can open room for some [edge](https://github.com/KhronosGroup/Vulkan-Docs/issues/1081) [cases](https://github.com/KhronosGroup/Vulkan-Docs/issues/1485) and the following is designed to give some common examples of what is and is not valid with push constants.

> Note: There are some CTS under `dEQP-VK.pipeline.push_constant.lifetime.*`

## Binding descriptor sets has no effect

Because push constants are not tied to descriptors the use of `vkCmdBindDescriptorSets` has no effect on the lifetime or [pipeline layout compatibility](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#descriptorsets-compatibility) of push constants.

## Mixing bind points

It is possible to use two different `VkPipelineBindPoint` that each have different uses of push constants in their shader

```cpp
// different ranges and therefore not compatible layouts
VkPipelineLayout layout_graphics; // VK_SHADER_STAGE_FRAGMENT_BIT
VkPipelineLayout layout_compute;  // VK_SHADER_STAGE_COMPUTE_BIT

// vkBeginCommandBuffer()
vkCmdBindPipeline(pipeline_graphics); // layout_graphics
vkCmdBindPipeline(pipeline_compute);  // layout_compute

vkCmdPushConstants(layout_graphics); // VK_SHADER_STAGE_FRAGMENT_BIT
// Still valid as the last pipeline and push constant for graphics are compatible
vkCmdDraw();

vkCmdPushConstants(layout_compute); // VK_SHADER_STAGE_COMPUTE_BIT
vkCmdDispatch(); // valid
// vkEndCommandBuffer()
```

## Binding non-compatible pipelines

The spec say:

> Binding a pipeline with a layout that is not compatible with the push constant layout does not disturb the push constant values.

The following examples helps illustrate this:

```cpp
// vkBeginCommandBuffer()
vkCmdPushConstants(layout_0);
vkCmdBindPipeline(pipeline_b); // non-compatible with layout_0
vkCmdBindPipeline(pipeline_a); // compatible with layout_0
vkCmdDraw(); // valid
// vkEndCommandBuffer()

// vkBeginCommandBuffer()
vkCmdBindPipeline(pipeline_b); // non-compatible with layout_0
vkCmdPushConstants(layout_0);
vkCmdBindPipeline(pipeline_a); // compatible with layout_0
vkCmdDraw(); // valid
// vkEndCommandBuffer()

// vkBeginCommandBuffer()
vkCmdPushConstants(layout_0);
vkCmdBindPipeline(pipeline_a); // compatible with layout_0
vkCmdBindPipeline(pipeline_b); // non-compatible with layout_0
vkCmdDraw(); // INVALID
// vkEndCommandBuffer()
```

## Layouts with no static push constants

It is also valid to have a shader with no use of push constants, such as

```glsl
void main() {
   gl_Position = vec4(1.0);
}
```

still use a layout that contains a `VkPushConstantRange`, as an example:

```cpp
VkPushConstantRange range = {VK_SHADER_STAGE_VERTEX_BIT, 0, 4};
VkPipelineLayoutCreateInfo pipeline_layout_info = {VK_SHADER_STAGE_VERTEX_BIT. 1, &range};
```

with a `VkPipeline` created with the above shader and pipeline layout, it is **still valid** to call `vkCmdPushConstants` on it.

The mental model can be thought of as `vkCmdPushConstants` is tied to the `VkPipelineLayout` used and therefore why they must match before a call such as `vkCmdDraw()`.

Just how one can bind descriptor sets that are never used by the shader, the same holds true for push constants.

## Updated incrementally

Push constants can be incrementally updated over the course of a command buffer.

The following shows an example of the values for a `vec4` example

```cpp
// vkBeginCommandBuffer()
vkCmdBindPipeline();
vkCmdPushConstants(offset: 0, size: 16, value = [0, 0, 0, 0]);
vkCmdDraw(); // values = [0, 0, 0, 0]

vkCmdPushConstants(offset: 4, size: 8, value = [1 ,1]);
vkCmdDraw(); // values = [0, 1, 1, 0]

vkCmdPushConstants(offset: 8, size: 8, value = [2, 2]);
vkCmdDraw(); // values = [0, 1, 2, 2]
// vkEndCommandBuffer()
```

## Pushing data with non-compatible layouts

In the following example, there will be two ranges that overlap each other with not compatible pipeline layouts

```cpp
// different ranges and therefore not compatible layouts
VkPushConstantRange range_a = {VK_SHADER_STAGE_VERTEX_BIT, 0, 16}; // layout_a
VkPushConstantRange range_b = {VK_SHADER_STAGE_VERTEX_BIT, 8, 16}; // layout_b
// 0   4   8   12  16  20  24
// [ a | a | a | a |   |   ]
// [   |   | b | b | b | b ]

// vkBeginCommandBuffer()
vkCmdPushConstants(layout_a, offset: 0, size: 16, value = [0, 0, 0, 0]);
vkCmdPushConstants(layout_b, offset: 8, size: 16, value = [1, 1, 1, 1]);
vkCmdPushConstants(layout_a, offset: 8, size: 8,  value = [2, 2]);

vkCmdBindPipeline(pipeline_a); // range_a
vkCmdDraw(); // value = [0, 2, 2, TODO]
// vkEndCommandBuffer()
```

// todo