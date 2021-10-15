import os

print("mappa neve:")
root = input()
dir = os.listdir(root)
f = open("dirnames.txt", mode="w")

for x in dir:
        f.write(root + "\\"+x + "," +'\n')
        print(root + "\\" +x)
print("mappanevek elmentve a getdirnames.txt-ben.")
f.close()

