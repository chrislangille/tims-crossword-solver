from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFilter, ImageMorph

# Load the image
path = "assets/ss3.png"
image = Image.open(path)

# Convert to grayscale
grayscale_image = image.convert("L")

# Invert the image
inverted_image = ImageOps.invert(ImageOps.expand(grayscale_image, border=1, fill=255))

# Manually adjust brightness and contrast
brightness_enhancer = ImageEnhance.Brightness(inverted_image)
brightened_image = brightness_enhancer.enhance(4.5)
contrast_enhancer = ImageEnhance.Contrast(brightened_image)
contrasted_image = contrast_enhancer.enhance(10.0)

# Convert to black and white (1-bit)
final_image = contrasted_image.convert("1")

bottom_start = 860

# draw rectangle over the top part of the image until the bottom_start
draw = ImageDraw.Draw(final_image)
draw.rectangle([0, 0, final_image.width, bottom_start], fill='white')
draw.rectangle([0, 0, 150, final_image.height], fill='white')
# draw rectangle over the right part of the image
draw.rectangle([final_image.width - 150, 0, final_image.width, final_image.height], fill='white')

draw.rectangle([0, final_image.height - 80, final_image.width, final_image.height], fill='white')

final_image = final_image.filter(ImageFilter.SHARPEN)
final_image = final_image.filter(ImageFilter.EDGE_ENHANCE)
final_image = final_image.filter(ImageFilter.MedianFilter())

final_image.save("assets/ss3_filtered.png")
final_image.show()











