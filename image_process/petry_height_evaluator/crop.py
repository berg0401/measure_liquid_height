import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog


class ImageCropper:
    def __init__(self, root, image_folder):
        self.root = root
        self.image_folder = image_folder
        self.images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.current_image_index = 0
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.crop_rect_id = None

        # Initialize canvas
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.load_image()

    def load_image(self):
        if self.current_image_index < len(self.images):
            image_path = os.path.join(self.image_folder, self.images[self.current_image_index])
            self.original_image = Image.open(image_path)
            self.display_image = ImageTk.PhotoImage(self.original_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
            self.root.title(f"Cropping: {self.images[self.current_image_index]}")
        else:
            self.root.quit()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.crop_rect_id:
            self.canvas.delete(self.crop_rect_id)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        if self.crop_rect_id:
            self.canvas.delete(self.crop_rect_id)
        self.crop_rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, curX, curY, outline='red')

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.save_crop()

    def save_crop(self):
        if None not in (self.start_x, self.start_y, self.end_x, self.end_y):
            box = (self.start_x, self.start_y, self.end_x, self.end_y)
            cropped_image = self.original_image.crop(box)
            cropped_image.save(os.path.join(self.image_folder, f"cropped_{self.images[self.current_image_index]}"))
            self.current_image_index += 1
            self.load_image()

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    image_folder = filedialog.askdirectory(title="Select Folder Containing Images")
    if image_folder:
        app = ImageCropper(root, image_folder)
        app.start()
    else:
        print("No folder selected.")