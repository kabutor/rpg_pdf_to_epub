import os
from collections import Counter

file_size = []
for filename in os.listdir('./images/'):
    filename = (os.path.join('images',filename))
    if (os.path.isfile( filename)):
        file_size.append(os.path.getsize(filename))
occur = Counter(file_size)
count = 0
for key,value in occur.items():
    if (value > 1):
        for filename in os.listdir('./images/'):
            filename = (os.path.join('images',filename))
            if (os.path.isfile( filename)):
                if (os.path.getsize(filename) == key):
                    os.remove(filename)
                    count+=1
print("Deleted %i duplicated images" % count)
