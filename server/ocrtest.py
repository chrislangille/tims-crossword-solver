import easyocr 

read = easyocr.Reader(['en'], gpu = False)
results = read.readtext('assets/ss3_filtered.png')
print(results) 
