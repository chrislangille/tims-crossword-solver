
from PIL import Image
from numpy.core.shape_base import block

# convert to rgb
block_color = "#907F75"
bg_color = "#E7DDCA"

space = 5
block_size = 49

block_color = (144, 127, 117, 255)
bg_color = (231, 221, 202, 255)

image = Image.open("assets/ss.png")
width = image.width
height = 500
offset_y = 300

# Crop the image to the word grid
image = image.crop((20, offset_y, width - 20, height + offset_y))

# the values that define the bounding box of the word grid
left_cutoff = 0
right_cutoff = 0
top_cutoff = 0
bottom_cutoff = 0

# Find the left cutoff

for x in range(image.width):
    for y in range(image.height):
        pixel = image.getpixel((x, y))
        if pixel == block_color:
            left_cutoff = x
            break
    if left_cutoff != 0:
        break

# Find the right cutoff
for x in range(image.width - 1, 0, -1):
    for y in range(image.height):
        pixel = image.getpixel((x, y))
        if pixel == block_color:
            right_cutoff = x
            break
    if right_cutoff != 0:
        break


# Find the top cutoff
for y in range(image.height):
    for x in range(image.width):
        pixel = image.getpixel((x, y))
        if pixel == block_color:
            top_cutoff = y
            break
    if top_cutoff != 0:
        break


# Find the bottom cutoff
for y in range(image.height - 1, 0, -1):
    for x in range(image.width):
        pixel = image.getpixel((x, y))
        if pixel == block_color:
            bottom_cutoff = y
            break
    if bottom_cutoff != 0:
        break


# Crop the image to the word grid
image = image.crop((left_cutoff, top_cutoff, right_cutoff, bottom_cutoff))



image.show()

matrix = []

for y in range(0, image.height, block_size + space):
    row = []
    i = 0
    for x in range(0, image.width, block_size + space):
        i += 1
        mid_y = y + block_size // 2 if y + block_size // 2 < image.height else image.height - 1
        mid_x = x + block_size // 2 if x + block_size // 2 < image.width else image.width - block_size // 2
        pixel = image.getpixel((mid_x, mid_y))
        if pixel == block_color:
            row.append(1)
        else:
            row.append(0)
    matrix.append(row)

words_counts = []
curr_count = 0

# Count the number of blocks in each row
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if matrix[i][j] == 1:
            curr_count += 1
            if j == len(matrix[0]) - 1:
                if curr_count > 2:
                    words_counts.append(curr_count)
        elif matrix[i][j] == 0 or j == len(matrix[0]) - 1:
            if curr_count > 2:
                words_counts.append(curr_count)
            curr_count = 0
    curr_count = 0

# Count the number of blocks in each column
for i in range(len(matrix[0])):
    for j in range(len(matrix)):
        if matrix[j][i] == 1:
            curr_count += 1
            if j == len(matrix) - 1:
                if curr_count > 2:
                    words_counts.append(curr_count)
        elif matrix[j][i] == 0 or j == len(matrix) - 1:
            if curr_count > 2:
                words_counts.append(curr_count)
                curr_count = 0
    curr_count = 0


# output to file 
with open('assets/word_grid.txt', 'w') as f:
    for count in words_counts:
        f.write(f"{count}\n")
    f.close()





