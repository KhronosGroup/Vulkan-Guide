# Pipeline Cache

Pipeline caching is a technique used with [VkPipelineCache](https://www.khronos.org/registry/vulkan/specs/1.1/html/vkspec.html#VkPipelineCache) objects to reuse pipelines that have already been created. Pipeline creation can be somewhat costly - it has to compile the shaders at creation time for example. The big advantage of a pipeline cache is that the pipeline state can be saved to a file to be used between runs of an application, eliminating some of the costly parts of creation. There is a great Khronos presentation on pipeline caching from [SIGGRAPH 2016](https://www.khronos.org/assets/uploads/developers/library/2016-siggraph/3D-BOF-SIGGRAPH_Jul16.pdf) ([video](https://www.youtube.com/watch?v=owuJRPKIUAg&t=1045s)) starting on slide 140.

![pipeline_cache_cache.png](../images/pipeline_cache_cache.png)

While pipeline caches are an important tool, it is important to create a robust system for them which Arseny Kapoulkine talks about in his [blog post](https://zeux.io/2019/07/17/serializing-pipeline-cache/).

To illustrate the performance gain and see a reference implementation of pipeline caches Khronos offers a [sample](https://github.com/KhronosGroup/Vulkan-Samples/tree/master/samples/performance/pipeline_cache) and [tutorial](https://github.com/KhronosGroup/Vulkan-Samples/blob/master/samples/performance/pipeline_cache/pipeline_cache_tutorial.md).
