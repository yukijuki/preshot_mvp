from PIL import Image
import os
import time

def create_image(imagedir, image_name)
    start = time.time()

    thumb = 30, 30
    small = 540, 540
    medium = 768, 768
    large = 1000, 1000
    xl = 1200, 1200

    image = image.open(os.path.join(image_dir, image_name))

    image_ext = image_name.split(".")[-1]
    image_name = image_name.split(".")[0]


    ## Thumbnail ##
    thumbnail_image = image.copy()
    thumbnail_image.thumbnail(thumb, Image.LANCZOS)
    thumbnail_image.save(f"{os.path.join(image_dir, image_name)}-thumbnail.{image_ext}", optimize=True, quality=95)

    ## Small ##
    small_image = image.copy()
    small_image.thumbnail(thumb, Image.LANCZOS)
    small_image.save(f"{os.path.join(image_dir, image_name)}-540.{image_ext}", optimize=True, quality=95)

    ## Medium ##
    medium_image = image.copy()
    medium_image.thumbnail(thumb, Image.LANCZOS)
    medium_image.save(f"{os.path.join(image_dir, image_name)}-768.{image_ext}", optimize=True, quality=95)

    ## Large ##
    large_image = image.copy()
    large_image.thumbnail(thumb, Image.LANCZOS)
    large_image.save(f"{os.path.join(image_dir, image_name)}-1000.{image_ext}", optimize=True, quality=95)

    ## XL ##
    xl_image = image.copy()
    xl_image.thumbnail(thumb, Image.LANCZOS)
    xl_image.save(f"{os.path.join(image_dir, image_name)}-1200.{image_ext}", optimize=True, quality=95)

    end = time.time()

    time_elapsed = end - start
    print(time_elapsed)
