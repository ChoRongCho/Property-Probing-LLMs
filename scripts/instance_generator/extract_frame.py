import os.path

import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk


class VideoToFramesGUI:
    def __init__(self,
                 master,
                 name="",
                 save_dir="",
                 video_path=None,
                 ):

        self.master = master
        self.master.title("Frame Extraction")

        self.frame_idx = 0
        self.video_path = video_path
        self.name = name
        self.save_dir = save_dir

        # check dir
        self.check_dir()
        self.capture = None
        self.save_count = 0

        self.canvas = tk.Canvas(self.master, width=640, height=480)
        self.canvas.pack()

        self.btn_open = tk.Button(self.master, text="Open Video", command=self.open_video)
        self.btn_open.pack()
        self.slider = ttk.Scale(self.master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_frame_idx)
        self.slider.pack(fill=tk.X)
        self.lbl_frame_number = tk.Label(self.master, text="Frame Number: 0")
        self.lbl_frame_number.pack()
        self.btn_save_frame = tk.Button(self.master, text="Save current frame", command=self.save_frame)
        self.btn_save_frame.pack()

        # Keyboard event
        self.master.bind("<Left>", lambda event: self.change_frame(-1))
        self.master.bind("<Right>", lambda event: self.change_frame(1))
        self.master.bind("<Up>", lambda event: self.change_frame(10))
        self.master.bind("<Down>", lambda event: self.change_frame(-10))
        self.master.bind("<period>", lambda event: self.change_frame(100))
        self.master.bind("<comma>", lambda event: self.change_frame(-100))

        self.master.bind("<Escape>", lambda event: self.master.quit())
        self.master.bind("<space>", lambda event: self.save_frame())

        self.open_video()

    def check_dir(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            print(f"{self.save_dir} created. ")
        else:
            print(f"{self.save_dir} already exists. ")

    def open_video(self):
        if not self.video_path:
            self.video_path = filedialog.askopenfilename()
        if self.video_path:
            self.capture = cv2.VideoCapture(self.video_path)
            self.slider.config(to=int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT)))
            self.next_frame()

    def set_frame_idx(self, value):
        self.frame_idx = int(float(value))
        self.next_frame()

    def change_frame(self, offset):
        self.frame_idx += offset
        self.slider.set(self.frame_idx)
        self.next_frame()

    def next_frame(self):
        if self.capture is not None:
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_idx)
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                self.photo = ImageTk.PhotoImage(image=image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
                self.lbl_frame_number.config(text=f"Frame Number: {self.frame_idx}")
            else:
                self.capture.release()

    def save_frame(self):
        if self.capture is not None:

            if self.save_count == 0:
                frame_path = os.path.join(self.save_dir, f"base_side.jpg")
            elif self.save_count == 1:
                frame_path = os.path.join(self.save_dir, f"probe_side.jpg")
            elif self.save_count == 2:
                frame_path = os.path.join(self.save_dir, f"recover_side.jpg")
            else:
                frame_path = os.path.join(self.save_dir, f"Capture_{self.name}_frame{self.frame_idx}.jpg")

            if frame_path:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_idx)
                ret, frame = self.capture.read()
                if ret:
                    cv2.imwrite(frame_path, frame)
                    self.save_count += 1
                    print(f"Frame {self.frame_idx} is saved. Total saved: {self.save_count}")


def main():
    obj = "obj14"

    source_folder = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/raw_data/" + obj + "/"
    result_folder = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/planning_v3_probe/" + obj + "/"
    video_name = obj + "_push_1.avi"
    video_path = os.path.join(source_folder, video_name)

    root = tk.Tk()
    app = VideoToFramesGUI(root,
                           video_path=video_path,
                           name="object3_top",
                           save_dir=result_folder)
    root.mainloop()


if __name__ == '__main__':
    main()
