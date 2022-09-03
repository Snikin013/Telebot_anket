text = ''

with open ('bad_words.txt', 'r') as i:
	with open('2.txt', 'w') as txt:
		for line in i:
			txt.write(line.replace(' ', '\n\n'))




exit()