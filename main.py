import os
import shutil
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

os.environ['TK_SILENCE_DEPRECATION'] = '1'

class ImageClassifier:
    def __init__(self, master):
        self.master = master
        self.master.title("图片分类标注软件")

        self.image_folder = None
        self.output_folder = None
        self.image_files = []
        self.current_image = None
        self.current_image_index = 0

        self.canvas = Canvas(master, width=400, height=400)
        self.canvas.grid(row=0, column=0)

        self.select_folder_button = Button(master, text="选择图片文件夹", command=self.select_image_folder)
        self.select_folder_button.grid(row=1, column=0)

        self.select_output_folder_button = Button(master, text="选择输出文件夹", command=self.select_output_folder)
        self.select_output_folder_button.grid(row=2, column=0)

        self.classify_button_1 = Button(master, text="类别 1", command=lambda: self.classify_image(1))
        self.classify_button_1.grid(row=1, column=2)

        self.classify_button_2 = Button(master, text="类别 2", command=lambda: self.classify_image(2))
        self.classify_button_2.grid(row=2, column=2)

        self.classify_button_3 = Button(master, text="类别 3", command=lambda: self.classify_image(3))
        self.classify_button_3.grid(row=3, column=2)

    def select_image_folder(self):
        self.image_folder = filedialog.askdirectory()
        self.image_files = [file for file in os.listdir(self.image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.load_image()

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()

    def load_image(self):
        if self.current_image_index < len(self.image_files):
            self.current_image = Image.open(os.path.join(self.image_folder, self.image_files[self.current_image_index]))
            self.current_image.thumbnail((400, 400))
            self.image_tk = ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(200, 200, anchor=CENTER, image=self.image_tk)
        else:
            self.canvas.create_text(200, 200, text="没有更多图片")

    def classify_image(self, category):
        if self.current_image and self.output_folder:
            output_category_folder = os.path.join(self.output_folder, str(category))
            if not os.path.exists(output_category_folder):
                os.makedirs(output_category_folder)

            src_path = os.path.join(self.image_folder, self.image_files[self.current_image_index])
            dest_path = os.path.join(output_category_folder, self.image_files[self.current_image_index])

            shutil.move(src_path, dest_path)
            self.current_image_index += 1
            self.load_image()

if __name__ == "__main__":
    root = Tk()
    app = ImageClassifier(root)
    root.mainloop()
