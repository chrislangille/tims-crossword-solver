import subprocess as process

# get args from command line
import sys
args = sys.argv
debug = len(args) > 1 and args[1] == "-d"

if debug:
    print("Debugging mode enabled")

if not debug:
    process.run(["python", "screencap.py"])

process.run(["python", "filter_img.py"])
process.run(["python", "letter_ocr.py"])

letters = []
# get letter_coords.txt
with open('assets/letter_coords.txt', 'r') as f:
    letter_coords = f.read().split('\n')
    for line in letter_coords:
        letter = line.split(":")
        if(letter[0] != ['']):
            letters.append(letter[0].lower())
    f.close()

# filter out non letters
for letter in letters:
    if not letter.isalpha():
        letters.remove(letter)

process.run(["python", "word_grid.py"])

word_grid_path = "assets/word_grid.txt"

# Read the word grid from the file
with open(word_grid_path, 'r') as f:
    word_grid = f.read().split('\n')
    f.close()

# filter out non letter
for word in word_grid:
    if not word.isnumeric():
        word_grid.remove(word)

print("Word Grid:", word_grid)

cmd = f"cd c && make && ./main {','.join(letters)} {','.join(word_grid)} words_alpha.txt"

# Run the combined command in the shell
process.run(cmd, shell=True, check=True)


