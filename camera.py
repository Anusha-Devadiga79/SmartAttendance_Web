import sys
import cv2
import os

if len(sys.argv) < 2:
    print("Student name required as argument.")
    sys.exit()

name = sys.argv[1]
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

cam = cv2.VideoCapture(0)
ret, frame = cam.read()
if ret:
    cv2.imshow("Student Capture", frame)
    cv2.imwrite(os.path.join(data_folder, f"{name}.png"), frame)
    print(f"Image saved as {name}.png")
    cv2.waitKey(1000)
else:
    print("Failed to capture image.")
cam.release()
cv2.destroyAllWindows()
