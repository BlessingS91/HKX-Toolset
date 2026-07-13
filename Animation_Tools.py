import json
from copy import deepcopy

# -------------------------
# Find max frame
# -------------------------


def get_max_frame(node):

    max_frame = -1

    if isinstance(node, dict):

        if len(node) > 0 and all(str(k).isdigit() for k in node.keys()):

            max_frame = max(int(k) for k in node.keys())

        for value in node.values():

            max_frame = max(max_frame, get_max_frame(value))

    elif isinstance(node, list):

        for item in node:

            max_frame = max(max_frame, get_max_frame(item))

    return max_frame


# -------------------------
# Trim frames
# -------------------------


def trim_frames(node, start_remove=0, end_limit=None):

    if isinstance(node, dict):

        if len(node) > 0 and all(str(k).isdigit() for k in node.keys()):

            new = {}

            for k, v in node.items():

                frame = int(k)

                if frame < start_remove:
                    continue

                if end_limit is not None and frame > end_limit:
                    continue

                new[str(frame - start_remove)] = v

            node.clear()
            node.update(new)

        else:

            for value in node.values():

                trim_frames(value, start_remove, end_limit)

    elif isinstance(node, list):

        for item in node:

            trim_frames(item, start_remove, end_limit)


# -------------------------
# Trim animation helper
# -------------------------


def trim_animation(data, start_trim, end_trim):

    data = deepcopy(data)

    max_frame = get_max_frame(data["actors"])

    new_end = max_frame - end_trim

    if new_end < start_trim:

        raise ValueError("Trim amount exceeds animation length")

    trim_frames(data["actors"], start_trim, new_end)

    data["length"] -= start_trim + end_trim

    return data


# =========================================================
# REVERSE ANIMATION
# =========================================================


def reverse_frames(node, max_frame):

    if isinstance(node, dict):

        # Frame dictionary
        if len(node) > 0 and all(str(k).isdigit() for k in node.keys()):

            new = {}

            for frame, value in node.items():

                reversed_frame = max_frame - int(frame)

                new[str(reversed_frame)] = value

            node.clear()
            node.update(new)

        else:

            for value in node.values():

                reverse_frames(value, max_frame)

    elif isinstance(node, list):

        for item in node:

            reverse_frames(item, max_frame)


def reverse_annotations(node, max_frame):

    if isinstance(node, dict):

        if "frame" in node and isinstance(node["frame"], int):

            node["frame"] = max_frame - node["frame"]

        for value in node.values():

            reverse_annotations(value, max_frame)

    elif isinstance(node, list):

        for item in node:

            reverse_annotations(item, max_frame)


def reverse_animation(file_path, output, log):

    try:

        log("Loading animation...")

        with open(file_path, "r", encoding="utf-8") as f:

            data = json.load(f)

        log("Finding animation length...")

        max_frame = get_max_frame(data["actors"])

        if max_frame < 0:

            raise ValueError("Could not find animation frames")

        log(f"Reversing {max_frame + 1} frames...")

        reverse_frames(data["actors"], max_frame)

        reverse_annotations(data, max_frame)

        with open(output, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4)

        return {"success": True, "message": "Animation reversed successfully."}

    except Exception as e:

        return {"success": False, "message": str(e)}


# -------------------------
# Merge nodes
# -------------------------


def merge_node(dst, src, offset):

    if (
        isinstance(dst, dict)
        and isinstance(src, dict)
        and len(src) > 0
        and all(str(k).isdigit() for k in src.keys())
    ):

        for frame, value in src.items():

            dst[str(int(frame) + offset)] = deepcopy(value)

        return

    if isinstance(dst, dict) and isinstance(src, dict):

        for key, value in src.items():

            if key not in dst:

                dst[key] = deepcopy(value)

            else:

                merge_node(dst[key], value, offset)

    elif isinstance(dst, list) and isinstance(src, list):

        for i in range(min(len(dst), len(src))):

            merge_node(dst[i], src[i], offset)


# -------------------------
# Shift annotations
# -------------------------


def shift_annotations(node, offset):

    if isinstance(node, dict):

        if "frame" in node and isinstance(node["frame"], int):

            node["frame"] += offset

        for value in node.values():

            shift_annotations(value, offset)

    elif isinstance(node, list):

        for item in node:

            shift_annotations(item, offset)


# -------------------------
# Main Merge Function
# -------------------------


def merge_animations(
    file_a, file_b, trim_start_a, trim_end_a, trim_start_b, trim_end_b, output, log
):

    try:

        log("Loading animations...")

        with open(file_a, "r", encoding="utf-8") as f:

            a = json.load(f)

        with open(file_b, "r", encoding="utf-8") as f:

            b = json.load(f)

        log("Trimming Animation A...")

        a = trim_animation(a, trim_start_a, trim_end_a)

        log("Trimming Animation B...")

        b = trim_animation(b, trim_start_b, trim_end_b)

        merged = deepcopy(a)

        offset = a["length"]

        merged["length"] = a["length"] + b["length"]

        log(f"Merging at frame offset {offset}")

        merge_node(merged["actors"], b["actors"], offset)

        shift_annotations(merged, offset)

        with open(output, "w", encoding="utf-8") as f:

            json.dump(merged, f, indent=4)

        return {"success": True, "message": "Animation merge complete."}

    except Exception as e:

        return {"success": False, "message": str(e)}

    # =========================================================


# SCALE / STRETCH ANIMATION
# =========================================================


def scale_frames(node, ratio):

    if isinstance(node, dict):

        # Frame dictionary
        if len(node) > 0 and all(str(k).isdigit() for k in node.keys()):

            new = {}

            for frame, value in node.items():

                new_frame = int(int(frame) * ratio)

                new[str(new_frame)] = value

            node.clear()
            node.update(new)

        else:

            for value in node.values():

                scale_frames(value, ratio)

    elif isinstance(node, list):

        for item in node:

            scale_frames(item, ratio)


def scale_annotations(node, ratio):

    if isinstance(node, list):

        # Annotation format:
        # [frame, "event"]

        if len(node) == 2 and isinstance(node[0], int):

            node[0] = int(node[0] * ratio)

        else:

            for item in node:

                scale_annotations(item, ratio)

    elif isinstance(node, dict):

        for value in node.values():

            scale_annotations(value, ratio)


def scale_animation(file_path, ratio, output, log):

    try:

        log("Loading animation...")

        with open(file_path, "r", encoding="utf-8") as f:

            data = json.load(f)

        if ratio <= 0:

            raise ValueError("Scale ratio must be greater than zero")

        log(f"Scaling animation by {ratio}x")

        scale_frames(data["actors"], ratio)

        if "annotations" in data:

            scale_annotations(data["annotations"], ratio)

        # Update animation length

        data["length"] = int(data["length"] * ratio)

        with open(output, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4)

        return {
            "success": True,
            "message": f"Animation scaled by {ratio}x successfully.",
        }

    except Exception as e:

        return {"success": False, "message": str(e)}
