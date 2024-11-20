import subprocess as process

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

cmd = f"cd c && make && ./main {','.join(letters)} 3,4,5,6 words_alpha.txt"

# Run the combined command in the shell
process = process.run(cmd, shell=True, check=True)

