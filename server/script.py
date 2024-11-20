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
    left_origin_row = None
    left_origin_col = None
    right_origin_row = None
    right_origin_col = None
    width = 0
    height = 0

    for col in range(0, mask_dimensions[1]):
        for row in range(0, mask_dimensions[0]):
            if img[row][col][0] != 0:
                left_origin_col = col
                break
        if left_origin_col != None:
            break

    if(left_origin_col == None):
        return (None, None), 0, 0

    for row in range(0, mask_dimensions[0]):
        for col in range(left_origin_col, left_origin_col + letter_dimensions[1]):
            if img[row][col][0] != 0:
                left_origin_row = row
                break
        if left_origin_row != None:
            break


    for col in range(mask_dimensions[1] - 1, -1, -1):
        for row in range(0, mask_dimensions[0]):
            if img[row][col][0] != 0:
                right_origin_col = col
                break
        if right_origin_col != None:
            break

    for row in range(0, mask_dimensions[0]):
        for col in range(right_origin_col, right_origin_col - letter_dimensions[1], -1):
            if img[row][col][0] != 0:
                right_origin_row = row
                break
        if right_origin_row != None:
            break

    origin = (left_origin_row, left_origin_col)
    width = right_origin_col - left_origin_col
    height = right_origin_row - left_origin_row


    return origin, width, height
    

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

