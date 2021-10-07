import os
from PIL import ImageFile, Image, ImageSequence

ImageFile.LOAD_TRUNCATED_IMAGES = True


def resize_image(image_filepath, width):
    path = os.path.split(image_filepath)[0]
    filename, ext = os.path.splitext(image_filepath)
    image = Image.open(image_filepath)

    if image.format == "GIF":
        target_filename = f"{filename}.jpg"
        tmp_filepath = os.path.join(path, target_filename)
        convert_gif(image, tmp_filepath)
        image = Image.open(tmp_filepath)
        target_filename = f"{filename}_sm.jpg"
        target_filepath = os.path.join(path, target_filename)
        resize_img(image, width, target_filepath)
        os.remove(tmp_filepath)
    else:
        if image.format == "PNG":
            image = image.convert("RGB")
        target_filename = f"{filename}_sm.jpg"
        target_filepath = os.path.join(path, target_filename)
        resize_img(image, width, target_filepath)

    return target_filepath


def convert_gif(image, target_filepath):
    new_image = image.convert("RGBA")
    new_image.load()

    background = Image.new("RGB", new_image.size, (255, 255, 255))
    background.paste(new_image, mask=new_image.split()[3])
    background.save(target_filepath, "JPEG", quality=80)


def resize_img(image, width, target_filepath):
    ratio = width / image.width
    img_resize = image.resize(
        (int(image.width * ratio), int(image.height * ratio)), Image.LANCZOS
    )
    img_resize.save(target_filepath, "JPEG", quality=95)


def resize_gif(image, width, target_filepath):
    ratio = width / image.width
    size = int(image.width * ratio), int(image.height * ratio)
    frames = ImageSequence.Iterator(image)

    def thumbnails(frames):
        for frame in frames:
            thumbnail = frame.copy()
            thumbnail.thumbnail(size, Image.ANTIALIAS)
            yield thumbnail

    frames = thumbnails(frames)

    # Save output
    om = next(frames)  # Handle first frame separately
    om.info = image.info  # Copy sequence info
    om.save(target_filepath, save_all=True, append_images=list(frames))
