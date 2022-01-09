from PIL import Image, ImageChops, ImageEnhance, ImageOps
import os, sys

def square_image(image, colortype='RGBA', bgcolor=(255,255,255)):
    width, height = image.size
    largest_dim = max([width, height])
    im_squared = Image.new(colortype, (largest_dim, largest_dim), bgcolor)
    im_squared.paste(image, 
        (
            int(largest_dim/2 - width/2), 
            int(largest_dim/2 - height/2), 
            int(largest_dim/2 + width/2),
            int(largest_dim/2 + height/2)
        ),
        mask=image)

    return im_squared

def png_to_jpg(image):
    return image.convert('RGB')

def resize(image, newdim):
    return image.resize(newdim, Image.ANTIALIAS)

def crop_surrounding_whitespace(image):
    bg = Image.new(image.mode, image.size, (255, 255, 255))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    if not bbox:
        return image
    return image.crop(bbox)

def increase_saturation(image, factor):
    converter = ImageEnhance.Color(image)
    image = converter.enhance(factor)
    return image

def increase_contrast(image, factor):
    converter = ImageEnhance.Contrast(image)
    image = converter.enhance(factor)
    return image

def make_greyscale(image):
    return image.convert('LA')

def flip_horizontal(image):
    return ImageOps.flip(image)

def flip_vertical(image):
    return ImageOps.mirror(image)

def process_images(image_dir, output_dir, to_image_type='jpg', square_images=True, destructive_resize=False):
    problem_files = []
    errors = []

    current_image_ix = 0
    for filename in os.listdir(image_dir):
        try:
            image = Image.open('{}/{}'.format(image_dir,filename)).convert('RGBA')
            image = make_greyscale(image)

            image = png_to_jpg(image)

            image.save('{}/{}.{}'.format(output_dir, current_image_ix, to_image_type))
            image = flip_horizontal(image)
            image.save('{}/{}.{}'.format(output_dir, current_image_ix+1, to_image_type))
            image = flip_vertical(image)
            image.save('{}/{}.{}'.format(output_dir, current_image_ix+2, to_image_type))
            image = flip_horizontal(image)
            image.save('{}/{}.{}'.format(output_dir, current_image_ix+3, to_image_type))
        except:
            print(str(sys.exc_info()))
            problem_files.append(filename)
            errors.append(str(sys.exc_info()[1]))
        current_image_ix+=4

process_images('./images/raw_images', './images/input')