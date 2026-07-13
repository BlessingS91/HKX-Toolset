# HKX Animation Toolkit

A utility toolkit for working with HKX animations exported from Smooth's HKX Editor.

This tool provides a collection of animation editing and HKX file management utilities designed to speed up Skyrim animation workflows.

## HKX File Tools

Requires a normal `.hkx` animation file.

### Duplicate Attacks
- Duplicates an attack animation into all 10 attack slots.
- Automatically detects and duplicates matching PowerAttack animations if they exist.

### Attack → PowerAttack
- Renames Attack animation files into PowerAttack animation files.
- Supports:
  - `mco_attack`
  - `bfco_attack`

### PowerAttack → Attack
- Renames PowerAttack animation files back into Attack animation files.
- Supports:
  - `mco_powerattack`
  - `bfco_powerattack`

Useful for quickly preparing and converting animation sets.

---

### Animation Merge
Combine two JSON animations together.

Features:
- Select Animation A and Animation B
- Remove starting frames from either animation
- Remove ending frames from either animation
- Export the merged animation as a new JSON file

Useful for:
- Creating animation chains
- Combining attack sequences
- Cleaning up transitions

---

### Reverse Animation

Reverse the direction of a JSON animation.

Features:
- Select a JSON animation
- Automatically reverse animation frames
- Export a reversed copy

Useful for:
- Creating mirrored animations
- Reusing existing animation data

---

### Stretch / Compress Animation

Adjust animation timing.

Features:
- Increase or decrease animation speed
- Preserve animation structure
- Export a scaled JSON animation

Examples:
