from PIL import Image, ImageDraw
import pytesseract

# Load the image
path = "assets/ss3_filtered.png"
filtered_image = Image.open(path)

# Create a copy of the original image to draw bounding boxes
draw_image = filtered_image.copy()
draw = ImageDraw.Draw(draw_image)

# Run OCR with Tesseract to get detailed information including bounding boxes
config = config = r'--psm 6 --oem 3 -c tessedit_create_boxfile=1 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
details = pytesseract.image_to_data(filtered_image, output_type=pytesseract.Output.DICT, config=config)

# Create a dictionary to store letter coordinates
letter_coords = {}
print(details)

# Iterate through the detected words and their letters
for i, text in enumerate(details['text']):
    if text.strip() and len(text) == 1:  # Only process single characters
        x = details['left'][i]
        y = details['top'][i]
        w = details['width'][i]
        h = details['height'][i]
        
        # Store coordinates
        letter_coords[text] = f"{x}, {y}"
        
        # Draw bounding box
        draw.rectangle([x, y, x+w, y+h], outline='green', width=2)

# Print the letter coordinates
print("Letter Coordinates:")
for letter, coords in letter_coords.items():
    print(f"{letter}: {coords}")

# Show the image with bounding boxes
draw_image.show()
