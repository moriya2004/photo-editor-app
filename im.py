import cv2
import math
from random import randint
from tkinter import filedialog, Tk
import numpy as np

class MyImage:
    def __init__(self, nameWindow, image_path):
        self.nameWindow = nameWindow
        self.image_path = image_path
        self.img = None
        self.action = None
        self.text_to_add = ""
        self.ix, self.iy = -1, -1
        self.load_image()  # Load the image before attempting to show it

    def load_image(self):
        self.img = cv2.imread(self.image_path)
        if self.img is None:
            raise ValueError("Failed to load image from path: {}".format(self.image_path))
        self.show_image()

    def show_image(self):
        cv2.imshow(self.nameWindow, self.img)
        cv2.setWindowTitle(self.nameWindow, "Image Viewer")
        self.update_mouse_callback()

    def update_mouse_callback(self):
        if self.action == "cut":
            cv2.setMouseCallback(self.nameWindow, self.cut)
        elif self.action == "add_text":
            cv2.setMouseCallback(self.nameWindow, self.add_text_on_click)
        elif self.action == "draw_triangle":
            cv2.setMouseCallback(self.nameWindow, self.add_triangle)
        elif self.action == "draw_rectangle":
            cv2.setMouseCallback(self.nameWindow, self.add_rectangle)
        elif self.action == "draw_circle":
            cv2.setMouseCallback(self.nameWindow, self.add_circle)
        else:
            cv2.setMouseCallback(self.nameWindow, lambda *args: None)

    def set_action(self, action):
        self.action = action
        self.update_mouse_callback()

    def cut(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ix = x
            self.iy = y
        elif event == cv2.EVENT_LBUTTONUP:
            # Ensure the coordinates are in the correct order
            x1, x2 = sorted([self.ix, x])
            y1, y2 = sorted([self.iy, y])
            # Crop the image using correct indexing
            cropped_image = self.img[y1:y2, x1:x2]
            self.img = cropped_image
            self.show_image()

    def add_text_on_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(self.img, self.text_to_add, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            cv2.imshow(self.nameWindow, self.img)

    def add_text(self, text):
        self.text_to_add = text
        self.set_action("add_text")

    def add_triangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ix = x
            self.iy = y
        elif event == cv2.EVENT_LBUTTONUP:
            new_x = randint(min(x, self.ix), max(x, self.ix)) + int(abs(self.ix - x) / 4)
            new_y = randint(min(y, self.iy), max(y, self.iy)) + int(abs(self.iy - y) / 4)
            cv2.line(self.img, (self.ix, self.iy), (x, y), (0, 165, 255), 2)
            cv2.line(self.img, (self.ix, self.iy), (new_x, new_y), (0, 165, 255), 2)
            cv2.line(self.img, (new_x, new_y), (x, y), (0, 165, 255), 2)
            cv2.imshow(self.nameWindow, self.img)

    def add_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ix = x
            self.iy = y
        elif event == cv2.EVENT_LBUTTONUP:
            cv2.rectangle(self.img, (self.ix, self.iy), (x, y), (0, 0, 0), 5)
            cv2.imshow(self.nameWindow, self.img)

    def add_circle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ix = x
            self.iy = y
        elif event == cv2.EVENT_LBUTTONUP:
            radius = math.sqrt((x - self.ix) ** 2 + (y - self.iy) ** 2)
            cv2.circle(self.img, (self.ix, self.iy), int(radius / 2), (255, 255, 255), 2)
            cv2.imshow(self.nameWindow, self.img)

    def apply_effect(self, effect):
        if effect == "Blur":
            self.img = cv2.blur(self.img, (5, 5))  # Example: Applying blur effect
        elif effect == "Contour":
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            self.img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # Example: Detecting contours
        elif effect == "Detail":
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            self.img = cv2.filter2D(self.img, -1, kernel)  # Example: Enhancing image details
        elif effect == "Sharpen":
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            self.img = cv2.filter2D(self.img, -1, kernel)  # Example: Sharpening image
        else:
            print("Unknown effect:", effect)
        self.show_image()

    def save_image(self):
        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, self.img)
            print("Image saved successfully at:", file_path)
        else:
            print("No location selected to save the image")

