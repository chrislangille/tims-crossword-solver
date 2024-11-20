from PIL import Image, ImageChops
import numpy

letter_dimensions = (78, 82)

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
    origin_row = None
    origin_col = None

    for col in range(0, mask_dimensions[1]):
        for row in range(0, mask_dimensions[0]):
            if img[row][col][0] != 0:
                origin_col = col
                break
        if origin_col != None:
            break

    if(origin_col == None):
        return (None, None), 0, 0

    for row in range(0, mask_dimensions[0]):
        for col in range(origin_col, origin_col + letter_dimensions[1]):
            if img[row][col][0] != 0:
                origin_row = row
                break
        if origin_row != None:
            break

    origin = (origin_row, origin_col)


    return origin, *letter_dimensions
    

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
i = 0
while origin[0] != None:    
    letter = Image.fromarray(numpy.uint8(filtered_letters))
    letter = letter.crop((origin[1], origin[0], origin[1] + width, origin[0] + height))
    letter.save('assets/letter' + str(i) + '.png')

    filtered_letters[origin[0]:origin[0] + height, origin[1]:origin[1] + width] = 0
    origin, width, height = find_letter_bounds(filtered_letters)
    i += 1



# Convert the result back to a PIL Image and save
result = Image.fromarray(numpy.uint8(filtered_letters))
result.save('assets/result.png')


