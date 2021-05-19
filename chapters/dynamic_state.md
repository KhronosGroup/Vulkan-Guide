# Pipeline Dynamic State

> [Vulkan Spec chapter](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#pipelines-dynamic-state)

## Overview

When creating a graphics `VkPipeline` object the logical flow for setting state is:

```cpp
// Using viewport state as an example
VkViewport viewport = {0.0, 0.0, 32.0, 32.0, 0.0, 1.0};

// Set value of state
VkPipelineViewportStateCreateInfo viewportStateCreateInfo;
viewportStateCreateInfo.pViewports = &viewport;
viewportStateCreateInfo.viewportCount = 1;

// Create the pipeline with the state value set
VkGraphicsPipelineCreateInfo pipelineCreateInfo;
pipelineCreateInfo.pViewportState = &viewportStateCreateInfo;
vkCreateGraphicsPipelines(pipelineCreateInfo, &pipeline);

vkBeginCommandBuffer();
// Select the pipeline and draw with the state's static value
vkCmdBindPipeline(pipeline);
vkCmdDraw();
vkEndCommandBuffer();
```

When the `VkPipeline` uses [dynamic state](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#pipelines-dynamic-state), some pipeline information can be omitted at creation time and instead set during recording of the command buffer. The new logical flow is:

```cpp
// Using viewport state as an example
VkViewport viewport = {0.0, 0.0, 32.0, 32.0, 0.0, 1.0};
VkDynamicState dynamicState = VK_DYNAMIC_STATE_VIEWPORT;

// not used now
VkPipelineViewportStateCreateInfo viewportStateCreateInfo;
viewportStateCreateInfo.pViewports = nullptr;
// still need to say how many viewports will be used here
viewportStateCreateInfo.viewportCount = 1;

// Set the state as being dynamic
VkPipelineDynamicStateCreateInfo dynamicStateCreateInfo;
dynamicStateCreateInfo.dynamicStateCount = 1;
dynamicStateCreateInfo.pDynamicStates = &dynamicState;

// Create the pipeline with state value not known
VkGraphicsPipelineCreateInfo pipelineCreateInfo;
pipelineCreateInfo.pViewportState = &viewportStateCreateInfo;
pipelineCreateInfo.pDynamicState = &dynamicStateCreateInfo;
vkCreateGraphicsPipelines(pipelineCreateInfo, &pipeline);

vkBeginCommandBuffer();
vkCmdBindPipeline(pipeline);
// Set the state for the pipeline at recording time
vkCmdSetViewport(viewport);
vkCmdDraw();
viewport.height = 64.0;
// set a new state value between draws
vkCmdSetViewport(viewport);
vkCmdDraw();
vkEndCommandBuffer();
```

## When to use dynamic state

> Note: Vulkan is a tool, so as with most things, and there is no single answer for this.

Some implementations might have a performance loss using some certain `VkDynamicState` state over a static value, but dynamic states might prevent an application from having to create many permutations of pipeline objects which might be a bigger desire for the application.

## What states are dynamic

The full list of possible dynamic states can be found in [VkDynamicState](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#VkDynamicState).

The `VK_EXT_extended_dynamic_state`, `VK_EXT_extended_dynamic_state2`, `VK_EXT_vertex_input_dynamic_state`, and `VK_EXT_color_write_enable` extensions were added with the goal to support applications that need to reduce the number of pipeline state objects they compile and bind.