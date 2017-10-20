#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid

from PIL import Image
from bbs.models import image_model


photo_specs = [
    {"type": "thumb", "width": 180, "height": 180, "quality": 86},
    {"type": "thumbicon", "is_square": True, "width": 100, "quality": 86},
    {"type": "title", "width": 800, "quality": 86},
    {"type": "photo", "length": 1080, "quality": 86},
]

pic_specs = [
    {"type": "mpic", "pixel": 14500, "quality": 88},
    {"type": "spic", "pixel": 6500, "quality": 88}
]


photo_type_dict = {
    "photo": {
        "sub_path": "photos",
        "specs": (
            {"type": "thumb", "width": 180, "height": 180, "quality": 86},
            {"type": "thumbicon", "is_square": True, "width": 100, "height": 100, "quality": 86},
            {"type": "title", "width": 800, "height": 200, "is_crop": True, "quality": 86},
            {"type": "photo", "width": 1080, "height": 1080, "quality": 86},
        ),
    },
    "avatar": {
        "sub_path": 'avatars',
        "specs": (
            {"type": "icon", "width": 200, "height": 200, "is_square": True, "quality": 86},
            {"type": "title", "width": 400, "height": 400, "is_square": True, "quality": 86},
        ),
    }
}


def convert_photo(photo_id, base_static_path, photo_type="photo"):
    f_path_raw = os.path.join(base_static_path, photo_type_dict[photo_type]["sub_path"],
                              "raw", photo_id[:2], photo_id + ".jpg")
    photo_raw_obj = Image.open(f_path_raw)
    photo_width, photo_height = photo_raw_obj.size
    photo_info_dict = {
        "id": str(photo_id), "width": photo_width, "height": photo_height,
        "size": str(float(os.path.getsize(f_path_raw)/1024))+"KB"
    }

    for spec in photo_type_dict[photo_type]["specs"]:
        d_path_target = os.path.join(
            base_static_path, photo_type_dict[photo_type]["sub_path"], spec["type"], photo_id[:2]
        )
        if not os.path.exists(d_path_target):
            os.makedirs(d_path_target, 0775)

        width_scale = float(photo_width / float(spec["width"]))
        height_scale = float(photo_height / float(spec["height"]))
        #print width_scale, height_scale
        size_box = None
        new_width = new_height = 0

        if "is_square" in spec and spec["is_square"]:
            if width_scale > 1 and height_scale > 1:
                if width_scale > height_scale:
                    # left, upper, right, lower
                    size_box = (int((photo_width - photo_height)/2), 0,
                        int((photo_width - photo_height)/2) + photo_height, photo_height)
                else:
                    size_box = (0, int((photo_height - photo_width)/2),
                        photo_width, photo_width+int(photo_height - photo_width)/2)
                new_width = spec["width"]
                new_height = spec["height"]
            else:
                if width_scale > height_scale:
                    size_box = (int((photo_width - photo_height)/2), 0,
                        int((photo_width - photo_height)/2)+photo_width, photo_height)
                    new_width = int(photo_height)
                    new_height = int(photo_height)
                else:
                    size_box = (0, int((photo_height - photo_width)/2),
                        photo_width, photo_width+int(photo_height-photo_width)/2)
                    new_width = int(photo_width)
                    new_height = int(photo_width)
        else:
            if width_scale > 1 or height_scale > 1:
                if width_scale > height_scale:
                    if height_scale > 1:
                        new_height = spec["height"]
                    else:
                        new_height = photo_height
                    new_width = int(photo_width * new_height / photo_height)
                else:
                    if width_scale > 1:
                        new_width = spec["width"]
                    else:
                        new_width = photo_width
                    new_height = int(photo_height * new_width / photo_width)
            else:
                new_width = int(photo_width)
                new_height = int(photo_height)

        # print spec, new_width, new_height

        f_path_target = os.path.join(d_path_target, photo_id + ".jpg")
        if size_box:
            region_obj = photo_raw_obj.crop(size_box)
            region_obj.resize((new_width, new_height), Image.ANTIALIAS).save(
                f_path_target, "JPEG", quality=spec["quality"]
            )
        else:
            photo_raw_obj.resize((new_width, new_height), Image.ANTIALIAS).save(
                f_path_target, "JPEG", quality=spec["quality"]
            )

    return photo_info_dict


def remove_photo(photo_id, base_static_path, photo_type="photo"):
    target_specs = photo_specs
    target_path_name = "photos"
    if photo_type == "pic":
        target_specs = pic_specs
        target_path_name = "pics"

    for spec in target_specs:
        f_path_target = os.path.join(base_static_path, target_path_name, spec["type"],
            photo_id[:2], photo_id + ".jpg"
        )
        try:
            os.remove(f_path_target)
        except OSError:
            pass


def save_upload_photo(photo_file, base_static_path, photo_type="photo"):
    photo_id = uuid.uuid4().hex

    d_path_raw = os.path.join(base_static_path, photo_type_dict[photo_type]["sub_path"],
                              "raw", photo_id[:2])
    f_path_raw = os.path.join(d_path_raw, photo_id+".jpg")
    if not os.path.exists(d_path_raw):
        os.makedirs(d_path_raw, 0755)
    with open(f_path_raw, "wb") as f:
        # f.write(photo_file["body"])
        f.write(photo_file)

    photo_info_dict = convert_photo(photo_id, base_static_path, photo_type=photo_type)
    image_model.insert_image({"image_id": photo_info_dict["id"]})
    return photo_info_dict
