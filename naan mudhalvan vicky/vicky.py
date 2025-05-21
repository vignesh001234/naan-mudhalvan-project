# Smart Parking Detection System

import cv2
import numpy as np

# Load image
img = cv2.imread('parkingslots.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5,5), 1)
edges = cv2.Canny(img_blur, 50, 150)

# Define parking spot coordinates (manually defined for your image)
# Format: [(x1, y1, x2, y2), ...] where (x1,y1) is top-left and (x2,y2) is bottom-right
parking_spots = [
    (31,350,127,468),
    (245,346,369,474),
    (470,327,599,468),
    (703,323,816,455),
    (920,317,1014,463),

]

def check_occupancy(spot):
    x1, y1, x2, y2 = spot
    roi = edges[y1:y2, x1:x2]
    # Count non-zero (edge) pixels in ROI
    non_zero_count = cv2.countNonZero(roi)
    # Threshold to decide if spot is occupied
    if non_zero_count > 500:  # tweak this value experimentally
        return True  # Occupied
    return False  # Free

# Visualize results with labels
for spot in parking_spots:
    occupied = check_occupancy(spot)
    color = (0,0,255) if occupied else (0,255,0)  # Red if occupied else green
    cv2.rectangle(img, (spot[0], spot[1]), (spot[2], spot[3]), color, 2)

    # Text to display
    label = "Occupied" if occupied else "Empty"

    # Position for text: slightly above top-left corner of the rectangle
    text_pos = (spot[0], spot[1] - 10 if spot[1] - 10 > 10 else spot[1] + 20)

    # Put text on image
    cv2.putText(img, label, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


cv2.imshow('Parking Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()



## Parking spots finding using click event

import cv2

# Load image
img = cv2.imread('image.png')
clone = img.copy()

# Variables to store points
points = []

def click_event(event, x, y, flags, param):
    global points, img

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point clicked: {x}, {y}")

        # Draw a small circle on clicked point
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

        # If two points are clicked, draw rectangle
        if len(points) == 2:
            cv2.rectangle(img, points[0], points[1], (255, 0, 0), 2)
            print(f"Rectangle from {points[0]} to {points[1]}")

        cv2.imshow("Image", img)

# Show image and set mouse callback
cv2.imshow("Image", img)
cv2.setMouseCallback("Image", click_event)

print("Click two points: top-left and bottom-right corners")

while True:
    key = cv2.waitKey(1) & 0xFF

    # Reset points on pressing 'r'
    if key == ord('r'):
        img = clone.copy()
        points = []
        print("Reset points. Click again.")

    # Exit on pressing 'q' or ESC
    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()