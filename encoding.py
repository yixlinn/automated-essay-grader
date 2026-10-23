# importing the chardet library to detect the file's encoding
import chardet

# opening the file in binary as chardet works with binary
with open('train.csv', 'rb') as file:
    raw_data = file.read()
    # detecting the encoding
    result = chardet.detect(raw_data)
    print(result)