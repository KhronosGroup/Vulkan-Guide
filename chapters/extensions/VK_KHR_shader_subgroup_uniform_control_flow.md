# VK_KHR_shader_subgroup_uniform_control_flow

## Overview

VK_KHR_shader_subgroup_uniform_control provides stronger guarantees for
reconvergence of invocations in a shader. If the extension is supported,
shaders can be modified to include a new attribute that provides the stronger
guarantees (see [GL_EXT_subgroup_uniform_control_flow](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_subgroup_uniform_control_flow.txt)). This attribute can only
be applied to shader stages that support subgroup operations (check the
subgroupSupportedStages feature in the VkPhysicalDeviceVulkan11Properties
struct).

The stronger guarantees cause the uniform control flow rules in the SPIR-V
specification to also apply to individual subgroups. The most important part of
those rules is the requirement to reconverge at a merge block if the all
invocations were converged upon entry to the header block. This is often
implicitly relied upon by shader authors, but not actually guaranteed by the
core Vulkan specification.

## Example

Consider the following GLSL snippet of a compute shader that attempts to reduce
the number of atomic operations from one per invocation to one per subgroup:

```glsl
// Free should be initialized to 0.
layout(set=0, binding=0) buffer BUFFER { uint free; uint data[]; } b;
void main() {
  bool needs_space = false;
  ...
  if (needs_space) {
    // gl_SubgroupSize may be larger than the actual subgroup size so
    // calculate the actual subgroup size.
    uvec4 mask = subgroupBallot(needs_space);
    uint size = subgroupBallotBitCount(mask);
    uint base = 0;
    if (subgroupElect()) {
      // "free" tracks the next free slot for writes.
      // The first invocation in the subgroup allocates space
      // for each invocation in the subgroup that requires it.
      base = atomicAdd(b.free, size);
    }
    
    // Broadcast the base index to other invocations in the subgroup.
    base = subgroupBroadcastFirst(base);
    // Calculate the offset from "base" for each invocation.
    uint offset = subgroupBallotExclusiveBitCount(mask);

    // Write the data in the allocated slot for each invocation that
    // requested space.
    b.data[base + offset] = ...;
  }
  ...
}
```

There is a problem with the code that might lead to unexpected results. Vulkan
only requires invocations to reconverge after the if statement that performs
the subgroup election if all the invocations in the __workgroup__ are converged at
that if statement. If the invocations don’t reconverge then the broadcast and
offset calculations will be incorrect. Not all invocations would write their
results to the correct index.

`VK_KHR_shader_subgroup_uniform_control_flow` can be utilized to make the shader
behave as expected in most cases. Consider the following rewritten version of
the example:

```glsl
// Free should be initialized to 0.
layout(set=0, binding=0) buffer BUFFER { uint free; uint data[]; } b;
// Note the addition of a new attribute.
void main() [[subroup_uniform_control_flow]] {
  bool needs_space = false;
  ...
  // Note the change of the condition.
  if (subgroupAny(needs_space)) {
    // gl_SubgroupSize may be larger than the actual subgroup size so
    // calculate the actual subgroup size.
    uvec4 mask = subgroupBallot(needs_space);
    uint size = subgroupBallotBitCount(mask);
    uint base = 0;
    if (subgroupElect()) {
      // "free" tracks the next free slot for writes.
      // The first invocation in the subgroup allocates space
      // for each invocation in the subgroup that requires it.
      base = atomicAdd(b.free, size);
    }

    // Broadcast the base index to other invocations in the subgroup.
    base = subgroupBroadcastFirst(base);
    // Calculate the offset from "base" for each invocation.
    uint offset = subgroupBallotExclusiveBitCount(mask);

    if (needs_space) {
      // Write the data in the allocated slot for each invocation that
      // requested space.
      b.data[base + offset] = ...;
    }
  }
  ...
}
```

The differences from the original shader are relatively minor. First, the
addition of the subgroup_uniform_control_flow attribute informs the
implementation that stronger guarantees are required by this shader. Second,
the first if statement no longer tests needs_space. Instead, all invocations in
the subgroup enter the if statement if any invocation in the subgroup needs to
write data. This keeps the subgroup uniform to utilize the enhanced guarantees
for the inner subgroup election.

There is a final caveat with this example. In order for the shader to operate
correctly in all circumstances, the subgroup must be uniform (converged) prior
to the first if statement.

## Related Extensions

* [GL_EXT_subgroup_uniform_control_flow](https://github.com/KhronosGroup/GLSL/blob/master/extensions/ext/GL_EXT_subgroup_uniform_control_flow.txt) - adds a GLSL attribute for entry points
  to notify implementations that stronger guarantees for convergence are
  required. This translates to a new execution mode in the SPIR-V entry point.
* [SPV_KHR_subgroup_uniform_control_flow](http://htmlpreview.github.io/?https://github.com/KhronosGroup/SPIRV-Registry/blob/master/extensions/KHR/SPV_KHR_subgroup_uniform_control_flow.html) - adds an execution mode for entry
  points to indicate the requirement for stronger reconvergence guarantees.
