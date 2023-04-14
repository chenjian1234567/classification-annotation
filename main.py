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
        
        # Add undo button
        self.undo_button = Button(master, text="撤销", command=self.undo_classification)
        self.undo_button.grid(row=4, column=0)

        # Initialize undo stack
        self.undo_stack = []
        
        # Add category counts label
        self.category_counts_text = Label(master, text="类别 1: 0 | 类别 2: 0 | 类别 3: 0")
        self.category_counts_text.grid(row=5, column=0, columnspan=4)


        self.canvas = Canvas(master, width=800, height=800)
        self.canvas.grid(row=0, column=0)

        self.select_folder_button = Button(master, text="选择图片文件夹", command=self.select_image_folder)
        self.select_folder_button.grid(row=1, column=0)

        self.select_output_folder_button = Button(master, text="选择输出文件夹", command=self.select_output_folder)
        self.select_output_folder_button.grid(row=2, column=0)

        self.classify_button_1 = Button(master, text="类别 1", command=lambda: self.classify_image(1))
        self.classify_button_1.grid(row=3, column=1)

        self.classify_button_2 = Button(master, text="类别 2", command=lambda: self.classify_image(2))
        self.classify_button_2.grid(row=3, column=2)

        self.classify_button_3 = Button(master, text="类别 3", command=lambda: self.classify_image(3))
        self.classify_button_3.grid(row=3, column=3)

        self.progress_text = Label(master, text="已标注：0 / 总数：0")
        self.progress_text.grid(row=3, column=0)

    def select_image_folder(self):
        self.image_folder = filedialog.askdirectory()
        self.image_files = [file for file in os.listdir(self.image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.load_image()
        self.update_progress()

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()

    def load_image(self):
        if self.current_image_index < len(self.image_files):
            self.current_image = Image.open(os.path.join(self.image_folder, self.image_files[self.current_image_index]))
            self.current_image.thumbnail((800, 800))
            self.image_tk = ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(400, 400, anchor=CENTER, image=self.image_tk)
        else:
            self.canvas.create_text(400, 400, text="没有更多图片")

    def classify_image(self, category):
        if self.current_image and self.output_folder:
            output_category_folder = os.path.join(self.output_folder, str(category))
            if not os.path.exists(output_category_folder):
                os.makedirs(output_category_folder)

            src_path = os.path.join(self.image_folder, self.image_files[self.current_image_index])
            dest_path = os.path.join(output_category_folder, self.image_files[self.current_image_index])

            shutil.move(src_path, dest_path)  # 使用 shutil.move()
            
            # Save the move to the undo stack
            self.undo_stack.append((dest_path, src_path))

            self.current_image_index += 1
            self.load_image()
            self.update_progress()

    def update_progress(self):
        progress_str = f"已标注：{self.current_image_index} / 总数：{len(self.image_files)}"
        self.progress_text.config(text=progress_str)
        
    def undo_classification(self):
        if self.undo_stack:
            last_move = self.undo_stack.pop()
            shutil.move(last_move[0], last_move[1])
            self.current_image_index -= 1
            self.load_image()
            self.update_progress()
            self.update_category_counts()  # Update category counts after undo

        
    def update_category_counts(self):
        if self.output_folder:
            category_counts = []
            for category in range(1, 4):
                output_category_folder = os.path.join(self.output_folder, str(category))
                if os.path.exists(output_category_folder):
                    image_count = len([f for f in os.listdir(output_category_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                else:
                    image_count = 0
                category_counts.append(image_count)

            counts_str = f"类别 1: {category_counts[0]} | 类别 2: {category_counts[1]} | 类别 3: {category_counts[2]}"
            self.category_counts_text.config(text=counts_str)

if __name__ == "__main__":
    root = Tk()
    app = ImageClassifier(root)
    root.mainloop()
