import os

print(os.getcwd())

path = os.getcwd().split("\\")
current_path = ""

for letter in path:
	if letter == "racer":
		path.remove(letter)

for letter in path:
	if letter == "dist":
		path.remove(letter)

for letter in path:
	current_path += letter + "/"