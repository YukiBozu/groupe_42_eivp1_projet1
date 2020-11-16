import csv

def transform_text_list(text):
    length = len(text)
    new_list = []
    new_entry = ""
    for i in range(length):
        if text[i] != ';':
            new_entry += text[i]
        elif text[i] == ';':
            new_list.append(new_entry)
            new_entry = ""
    new_list.append(new_entry)
    return new_list
with open('EIVP_KM.csv', newline='') as File:
    reader = csv.reader(File)
    File_list = []
    File_text = []
    for row in reader:
        File_text.append(row)
        File_list.append(transform_text_list(row[0]))

print(File_list[1])