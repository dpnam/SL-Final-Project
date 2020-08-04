import os
import cv2

location = {}
with open(os.path.join("GreenParking", "location.txt")) as f:
    for line in f:
        line = line.strip()
        parts = line.split()
        if len(parts) == 0:
            break
        file = parts[0]

        x = int(parts[2])
        y = int(parts[3])
        w = int(parts[4])
        h = int(parts[5])

        x2, y2 = x + w, y + h

        location[file] = (x, y, x2, y2)



ROOT_DIR = "characters"

_, dirs, _ = next(os.walk(ROOT_DIR))

for dir in dirs:
    for subdirs, _, files in os.walk(os.path.join(ROOT_DIR, dir)):
        for file in files:
            if file.endswith('.jpg'):
                filepath = os.path.join(subdirs, file)
                im = cv2.imread(filepath)
                x1, y1, x2, y2 = location[file]
                cv2.imwrite(filepath, im[y1:y2, x1:x2])


