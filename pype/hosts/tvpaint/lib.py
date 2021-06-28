from PIL import Image

import avalon.io
import avalon.tvpaint.lib


def composite_images(input_image_paths, output_filepath):
    """Composite images in order from passed list.

    Raises:
        ValueError: When entered list is empty.
    """
    if not input_image_paths:
        raise ValueError("Nothing to composite.")

    img_obj = None
    for image_filepath in input_image_paths:
        _img_obj = Image.open(image_filepath)
        if img_obj is None:
            img_obj = _img_obj
        else:
            img_obj.alpha_composite(_img_obj)
    img_obj.save(output_filepath)


def set_context_settings(asset):
    project = avalon.io.find_one({"_id": asset["parent"]})

    framerate = asset["data"].get("fps", project["data"].get("fps"))
    if framerate:
        avalon.tvpaint.lib.execute_george(
            "tv_framerate {} \"timestretch\"".format(framerate)
        )
    else:
        print("Framerate was not found!")

    width_key = "resolutionWidth"
    height_key = "resolutionHeight"
    width = asset["data"].get(width_key, project["data"].get(width_key))
    height = asset["data"].get(height_key, project["data"].get(height_key))
    if width and height:
        avalon.tvpaint.lib.execute_george(
            "tv_resizepage {} {} 0".format(width, height)
        )
    else:
        print("Resolution was not found!")

    frame_start = asset["data"].get("frameStart")
    frame_end = asset["data"].get("frameEnd")

    if frame_start is None or frame_end is None:
        print("Frame range was not found!")
        return

    handles = asset["data"].get("handles") or 0
    handle_start = asset["data"].get("handleStart")
    handle_end = asset["data"].get("handleEnd")
    if handle_start is None or handle_end is None:
        handle_start = handle_end = handles

    # Always start from 0 Mark In and set only Mark Out
    mark_in = 0
    mark_out = mark_in + (frame_end - frame_start) + handle_start + handle_end

    avalon.tvpaint.lib.execute_george("tv_markin {} set".format(mark_in))
    avalon.tvpaint.lib.execute_george("tv_markout {} set".format(mark_out))