# VK_EXT_shader_subgroup_*

`VK_EXT_shader_subgroup_ballot` and `VK_EXT_shader_subgroup_vote` were the original efforts to expose subgroups in Vulkan. If you are using Vulkan 1.1 or greater, there is no need to use these extensions and instead use the built in core API to query for subgroup support.

For more information about the current subgroup support, there is a great [Khronos blog post](https://www.khronos.org/blog/vulkan-subgroup-tutorial) as well as a presentation from Vulkan Developer Day 2018 ([slides](https://www.khronos.org/assets/uploads/developers/library/2018-vulkan-devday/06-subgroups.pdf) and [video](https://www.youtube.com/watch?v=8MyqQLu_tW0)).