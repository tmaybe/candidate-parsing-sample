import csv
import re

########### MAIN ###########

output_file = open("out-stripped.csv", 'a')
output_writer = csv.writer(output_file)

input_filename = 'PLANO DCT DIY 1.csv'

with open(input_filename, 'rU') as infile:
    for input_row in csv.reader(infile):
        for input_pos in range(len(input_row)):
            input_row[input_pos] = re.sub('\n', ' ', input_row[input_pos])

        output_writer.writerow(input_row)

# done writing, close the file
output_file.close()
