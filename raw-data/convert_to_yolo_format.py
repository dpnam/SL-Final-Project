import os
import cv2

FILE_DIR = "GreenParking"

with open(os.path.join(FILE_DIR, "classes.txt"), "w") as f:
    f.write("plate")

with open(os.path.join(FILE_DIR, "location.txt")) as fIn:
    for line in fIn:
        line = line.strip()
        parts = line.split()
        if len(parts) == 0:
            break

        file = parts[0]

        im = cv2.imread(os.path.join(FILE_DIR, file))

        im_h, im_w = im.shape[:2]

        file_name, ext = os.path.splitext(file)

        count = int(parts[1])
        with open(os.path.join(FILE_DIR, f"{file_name}.txt"), 'w') as fOut:
            for i in range(count):
                x = int(parts[2 + i*4])
                y = int(parts[3 + i*4])
                w = int(parts[4 + i*4])
                h = int(parts[5 + i*4])

                xCenter = x + w / 2
                yCenter = y + h / 2

                # tweak
                fOut.write(f"0 {xCenter / im_w} {yCenter/im_h} {w/im_w} {h/im_h}\n")
