import re

with open("calon-dprd_diy.csv", 'rU') as f:
	for line in f:
		if re.search(r'[\x80-\xFF]', line):
			print 'bad string in line ' + line
