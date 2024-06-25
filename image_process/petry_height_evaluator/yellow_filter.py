import os
from PIL import Image
import cv2
import copy
import numpy as np
import sys
import tkinter as tk
from tkinter import filedialog


class YellowFilter:
    def __init__(self,image_folder):
        self.filtered_images = None
        self.image_folder = image_folder
        self.images_name = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.current_image_index = 0


    def filter(self):
        self.images = []
        self.filtered_images=[]
        self.median_images=[]
        for image_name in self.images_name:
            image = self.convert_png_to_rgb(image_name)
            self.images.append(image)

        self.filtered_images = copy.deepcopy(self.images)
        for image in self.filtered_images:
            self.get_yellow_pixels(image)
        for image in self.filtered_images:
            median_blured = cv2.medianBlur(image, 9)
            self.median_images.append(median_blured)
        for image_index in range(len(self.filtered_images)):
            compared_image = self.show_compared_image(self.filtered_images[image_index], self.median_images[image_index], self.images[image_index])
            self.save_compared_image(compared_image, self.images_name[image_index])
    def show_compared_image(self,image1,image2,image3):
        compare_figure = cv2.hconcat([image1,image2,image3])
        cv2.imshow('RGB Image', compare_figure)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()
        return compare_figure
    def save_compared_image(self,image,image_name):
        cv2.imwrite(rf"C:\Users\15142\OneDrive - USherbrooke\S7\STAGE-T5\VISION\filtered_only\{image_name}", image)

    def get_yellow_pixels(self,image):
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if image[x][y][0] <= 40 or image[x][y][0] >= 100 or image[x][y][1] <= 50 or image[x][y][1] >= 100 or \
                        image[x][y][2] <= 80 or image[x][y][2] >= 130:
                    image[x][y] = [0, 0, 0]
                else:
                    image[x][y] = [255, 255, 255]
    def convert_png_to_rgb(self,image_name):
        # Read the image
        img_path = os.path.join(self.image_folder, image_name)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Use COLOR_BGRA2BGR if the input image has alpha channel
        return rgb_img

if __name__ == "__main__":
    image_folder = r"C:\Users\15142\OneDrive - USherbrooke\S7\STAGE-T5\VISION\3d_piece_simulation" #filedialog.askdirectory(title="Select Folder Containing Images")
    if image_folder:
        app = YellowFilter(image_folder)
        app.filter()
    else:
        print("No folder selected.")