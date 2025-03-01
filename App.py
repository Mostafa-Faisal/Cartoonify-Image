import cv2
import pathlib
import pyautogui
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import webbrowser


class ImageProcessor:
    def __init__(self, root):
        self.window = root
        self.window.geometry("940x580")
        self.window.title('Cartoonify Image')
        self.window.resizable(width=False, height=False)

        self.width = 700
        self.height = 540

        self.Image_Path = ''
        self.ProcessedImg = ''

        # Creating Menubar
        self.menubar = Menu(self.window)

        # Adding File Menu and its submenus
        file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open Image', command=self.open_image)

        # Adding Process Menu and its submenus
        process_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Process', menu=process_menu)
        process_menu.add_command(label='Cartoonify', command=self.cartoonify)
        process_menu.add_command(label='Pencil Sketch', command=self.create_pencil_sketch)

        # Adding Share Menu and its submenus
        share_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Share', menu=share_menu)
        share_menu.add_command(label='Share on Facebook', command=self.share_on_facebook)
        share_menu.add_command(label='Share on Twitter', command=self.share_on_twitter)
        share_menu.add_command(label='Share on WhatsApp', command=self.share_on_whatsapp)

        # Adding Exit Option in the Main Menu Bar
        self.menubar.add_command(label='Exit', command=self._exit)

        # Configuring the menubar
        self.window.config(menu=self.menubar)

        # Creating a Frame
        self.frame_1 = Frame(self.window, width=self.width, height=self.height)
        self.frame_1.pack()
        self.frame_1.place(anchor='center', relx=0.5, rely=0.5)

        # Create and configure "Open Image" button
        self.open_image_button = Button(self.frame_1, text="Open Image", command=self.open_image, bg="green", fg="white", font=("Arial", 16), width=20, height=2)
        self.open_image_button.pack()

    def open_image(self):
        self.clear_screen()
        self.Image_Path = filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                                      filetypes=(("Image files", "*.jpg *.jpeg *.png"),))
        if len(self.Image_Path) != 0:
            self.show_image(self.Image_Path)

    def show_image(self, img_path):
        image = Image.open(img_path)
        resized_image = image.resize((self.width, self.height))
        self.img = ImageTk.PhotoImage(resized_image)
        label = Label(self.frame_1, image=self.img)
        label.pack()

    def cartoonify(self):
        img_path = self.Image_Path
        if len(img_path) == 0:
            pass
        else:
            img = cv2.imread(img_path)
            img = cv2.resize(img, (740, 480))
            gray_img = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
            smooth_img = cv2.medianBlur(src=gray_img, ksize=5)
            edges = cv2.adaptiveThreshold(src=smooth_img, maxValue=255,
                                          adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C, thresholdType=cv2.THRESH_BINARY,
                                          blockSize=9, C=9)
            color_img = cv2.bilateralFilter(src=img, d=9, sigmaColor=300, sigmaSpace=300)
            cartoon_img = cv2.bitwise_and(src1=color_img, src2=color_img, mask=edges)

            # Save option for cartoonified image
            save_option = messagebox.askquestion("Save Cartoonified Image", "Do you want to save the cartoonified image?")
            if save_option == 'yes':
                filename = pyautogui.prompt("Enter the filename to be saved")
                filename = filename + pathlib.Path(img_path).suffix
                cv2.imwrite(filename, cartoon_img)

            # Display cartoonified image in a new window
            cartoon_window = Toplevel(self.window)
            cartoon_window.title("Cartoonified Image")
            cartoon_window.geometry(f"{img.shape[1]}x{img.shape[0]}")  # Set window size based on image dimensions

            # Convert image to RGB format for compatibility with Tkinter
            cartoon_img_rgb = cv2.cvtColor(cartoon_img, cv2.COLOR_BGR2RGB)
            cartoon_img_pil = Image.fromarray(cartoon_img_rgb)
            cartoon_img_tk = ImageTk.PhotoImage(cartoon_img_pil)

            # Create a Label widget to display the cartoonified image
            label = Label(cartoon_window, image=cartoon_img_tk)
            label.pack()

            # Keep a reference to the image to prevent it from being garbage collected
            label.image = cartoon_img_tk

    def create_pencil_sketch(self):
        img_path = self.Image_Path
        if len(img_path) == 0:
            pass
        else:
            img = cv2.imread(img_path)
            img = cv2.resize(img, (740, 480))
            gray_img = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
            invert_img = cv2.bitwise_not(gray_img)
            intensity = 37  # You can adjust the intensity as needed
            smooth_img = cv2.medianBlur(src=invert_img, ksize=intensity)
            ivt_smooth_img = cv2.bitwise_not(smooth_img)
            sketch_img = cv2.divide(gray_img, ivt_smooth_img, scale=250)

            # Save option for sketch image
            save_option = messagebox.askquestion("Save Pencil Sketch", "Do you want to save the pencil sketch?")
            if save_option == 'yes':
                filename = pyautogui.prompt("Enter the filename to be saved")
                filename = filename + pathlib.Path(img_path).suffix
                cv2.imwrite(filename, sketch_img)

            # Display sketch image in a new window
            sketch_window = Toplevel(self.window)
            sketch_window.title("Pencil Sketch")
            sketch_window.geometry(f"{img.shape[1]}x{img.shape[0]}")  # Set window size based on image dimensions

            # Convert image to RGB format for compatibility with Tkinter
            sketch_img_rgb = cv2.cvtColor(sketch_img, cv2.COLOR_BGR2RGB)
            sketch_img_pil = Image.fromarray(sketch_img_rgb)
            sketch_img_tk = ImageTk.PhotoImage(sketch_img_pil)

            # Create a Label widget to display the sketch image
            label = Label(sketch_window, image=sketch_img_tk)
            label.pack()

            # Keep a reference to the image to prevent it from being garbage collected
            label.image = sketch_img_tk

    def clear_screen(self):
        for widget in self.frame_1.winfo_children():
            widget.destroy()

    def _exit(self):
        self.window.destroy()

    def share_on_facebook(self):
        if self.Image_Path:
            webbrowser.open("https://www.facebook.com/sharer/sharer.php?u=" + self.Image_Path)

    def share_on_twitter(self):
        if self.Image_Path:
            webbrowser.open("https://twitter.com/intent/tweet?url=" + self.Image_Path)

    def share_on_whatsapp(self):
        if self.Image_Path:
            webbrowser.open("https://wa.me/?text=Check%20out%20this%20image:%20" + self.Image_Path)

if __name__ == "__main__":
    root = Tk()
    obj = ImageProcessor(root)
    root.mainloop()
