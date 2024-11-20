from PIL import Image, ImageChops
import numpy

#only keep the white pixels
def whites_only(bg):
    # Create a mask for the white pixels
    mask = numpy.all(bg == [255, 255, 255, 255], axis=-1)

    # Create a new array with the white pixels
    result = numpy.zeros_like(bg)
    result[mask] = bg[mask]

    return result

def find_letter_bounds(img):
    origin = None

    # find top left corner
    for row in range(0, mask_dimensions[0]):
        for col in range(0, mask_dimensions[1]):
            if img[row][col][0] != 0:
                origin = (row, col)
                break
        if origin != None:
            break

    return origin, 80, 80
    

# Load images
ss = Image.open('assets/ss.PNG')
mask_dimensions = (650, 650)

# Convert images to RGBA (adds alpha channel)
ss = ss.convert('RGBA')
ss = ImageChops.offset(ss, -260, -1750)
ss = ss.crop((0, 0, *mask_dimensions))
ss_array = numpy.array(ss).astype(float)

# Apply 'hard mix' blending
filtered_letters = whites_only(ss_array)

origin, width, height = find_letter_bounds(filtered_letters)
print(origin, width, height)

# create image of letter_dimensions
letter = Image.fromarray(numpy.uint8(filtered_letters))
letter =  letter.crop((origin[1], origin[0], origin[1] + width, origin[0] + height))
letter.save('assets/letter.png')


# Convert the result back to a PIL Image and save
result = Image.fromarray(numpy.uint8(filtered_letters))
result.save('assets/result.png')


