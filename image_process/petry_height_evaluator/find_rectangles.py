import os
import cv2
import numpy as np
import copy



class findRectangles:
    def __init__(self,image_folder):
        self.image_folder = image_folder
        self.images_name = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.current_image_index = 0


    def find(self):
        self.images = []
        for image_name in self.images_name:
            image = self.convert_png_to_rgb(image_name)
            self.images.append(image)
        for image in self.images:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            possible_rectangles = []
            self.find_possible_rectangles(contours, possible_rectangles)
            if len(possible_rectangles) >> 0:
                biggest_rectangle = self.get_biggest_rectangle(possible_rectangles)
                x, y, w, h = cv2.boundingRect(biggest_rectangle)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow('Rectangles Detected', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("No rectangles found")
    def find_possible_rectangles(self,contours,possible_rectangles):
        for contour in contours:
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            # Check if polygon has 4 corners (assuming it's a rectangle)
            if len(approx) == 4:
                possible_rectangles.append(contour)

    def get_biggest_rectangle(self,possible_rectangles):
        max_area = 0
        biggest_rectangle = None
        for rectangle in possible_rectangles:
            area = cv2.contourArea(rectangle)
            if area >= max_area:
                max_area = area
                biggest_rectangle = rectangle
        return biggest_rectangle

    def show_compared_image(self,image1,image2):
        compare_figure = cv2.hconcat([image1,image2])
        cv2.imshow('RGB Image', compare_figure)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()
        return compare_figure
    def save_compared_image(self,image,image_name):
        cv2.imwrite(rf"C:\Users\15142\OneDrive - USherbrooke\S7\STAGE-T5\VISION\find_rectangles\{image_name}", image)
    def convert_png_to_rgb(self,image_name):
        # Read the image
        img_path = os.path.join(self.image_folder, image_name)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Use COLOR_BGRA2BGR if the input image has alpha channel
        return rgb_img

if __name__ == "__main__":
    image_folder = r"C:\Users\15142\OneDrive - USherbrooke\S7\STAGE-T5\VISION\filtered_only" #filedialog.askdirectory(title="Select Folder Containing Images")
    if image_folder:
        app = findRectangles(image_folder)
        app.find()
    else:
        print("No folder selected.")