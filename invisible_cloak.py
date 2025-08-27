import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)

time.sleep(10)

for i in range(30):
    ret, frame = cap.read()

background = 0      
for i in range(60):
    ret, background = cap.read()
    if ret:
        background = np.flip(background, axis=1)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = np.flip(img, axis=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_olive = np.array([40, 40, 40])
    upper_olive = np.array([70, 255, 255])

    mask = cv2.inRange(hsv, lower_olive, upper_olive)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    cloak_area = cv2.bitwise_and(background, background, mask=mask)

    mask_inv = cv2.bitwise_not(mask)
    rest_area = cv2.bitwise_and(img, img, mask=mask_inv)

    final_img = cv2.addWeighted(cloak_area, 1, rest_area, 1, 0)

    cv2.imshow("Invisible Cloak", final_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
