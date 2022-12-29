import os

texts = []

input_ = open("input.txt", 'w')
for file in os.listdir("frames"):
    texts.append("frames/"+file)
input_.write("\n".join(texts))
input_.close()