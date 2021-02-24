import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import matplotlib.pyplot as plt
import os
import random

class MainWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        menu = tk.Menu(self.master)
        master.config(menu=menu)

        file_menu = tk.Menu(menu)
        file_menu.add_command(label="Open", command=self.openFile)
        file_menu.add_command(label="Save", command=self.saveFile)
        file_menu.add_command(label="Save As", command=self.saveAsFile)
        file_menu.add_command(label="Exit", command=self.quit)
        menu.add_cascade(label="File", menu=file_menu)

        instruments = tk.Menu(menu)
        instruments.add_command(label="Histogram", command=self.histogram)
        instruments.add_command(label="Rotate", command=lambda: RotateWindow(self, self.get_coords()))
        instruments.add_command(label="Resize", command=lambda: ResizeWindow(self, self.get_coords()))
        instruments.add_command(label="Scale", command=lambda: ScaleWindow(self, self.get_coords()))
        menu.add_cascade(label="Instruments", menu=instruments)

        filters = tk.Menu(menu)
        filters.add_command(label="Blur", command=self.blur)
        filters.add_command(label="Hue", command=self.hue)
        filters.add_command(label="MinFilter", command=self.min_filter)
        filters.add_command(label="MaxFilter", command=self.max_filter)
        filters.add_command(label="ModeFilter", command=self.mode_filter)
        menu.add_cascade(label="Filters", menu=filters)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=True)
        self.image = None # none yet

    def get_coords(self):
        self.master.update_idletasks()
        coords = self.master.geometry()
        coords = coords.split('+')
        width_window, height_window = int(coords[1]), int(coords[2])
        return [width_window, height_window]

    #Where I open my file
    def openFile(self):
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File",
                                              filetypes=[("JPG Files","*.jpg"), ("JPEG Files","*.jpeg"), ("PNG Files","*.png"), ("BMP Files","*.bmp")])
        if not self.filename:
            return # user cancelled; stop this method

        self.load = Image.open(self.filename)
        w, h = self.load.size
        self.render = ImageTk.PhotoImage(self.load)  # must keep a reference to this

        if self.image is not None:  # if an image was already loaded
            self.canvas.delete(self.image)  # remove the previous image

        self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)

        root.geometry("%dx%d" % (w, h))

    def saveFile(self):
        self.load.save(self.filename)

    def saveAsFile(self):
        self.filename = filedialog.asksaveasfilename(title = "Select file", defaultextension=".png", filetypes = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),
                                                                                                         ('PNG', '*.png'),('BMP', ('*.bmp','*.jdib'))))
        if not self.filename:
            return # user cancelled; stop this method
        self.load.save(self.filename)

    def blur(self):
        self.load = self.load.filter(ImageFilter.BLUR)
        w, h = self.load.size
        self.render = ImageTk.PhotoImage(self.load)  # must keep a reference to this

        if self.image is not None:  # if an image was already loaded
            self.canvas.delete(self.image)  # remove the previous image

        self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)

    def hue(self):
        w, h = self.load.size
        draw = ImageDraw.Draw(self.load)
        pix = self.load.load()
        for i in range(w):
             for j in range(h):
                 rand = random.randint(-70, 70)
                 a = pix[i, j][0] + rand
                 b = pix[i, j][1] + rand
                 c = pix[i, j][2] + rand
                 if (a < 0):
                     a = 0
                 if (b < 0):
                     b = 0
                 if (c < 0):
                     c = 0
                 if (a > 255):
                     a = 255
                 if (b > 255):
                     b = 255
                 if (c > 255):
                     c = 255
                 draw.point((i, j), (a, b, c))
        self.render = ImageTk.PhotoImage(self.load)  # must keep a reference to this

        if self.image is not None:  # if an image was already loaded
            self.canvas.delete(self.image)  # remove the previous image

        self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)

    def min_filter(self):
        self.load = self.load.filter(ImageFilter.MinFilter)
        w, h = self.load.size
        self.render = ImageTk.PhotoImage(self.load)  # must keep a reference to this

        if self.image is not None:  # if an image was already loaded
            self.canvas.delete(self.image)  # remove the previous image

        self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)

    def max_filter(self):
        self.load = self.load.filter(ImageFilter.MaxFilter)
        w, h = self.load.size
        self.render = ImageTk.PhotoImage(self.load)  # must keep a reference to this

        if self.image is not None:  # if an image was already loaded
            self.canvas.delete(self.image)  # remove the previous image

        self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)

    def mode_filter(self):
        self.load = self.load.filter(ImageFilter.ModeFilter)
        w, h = self.load.size
        self.render = ImageTk.PhotoImage(self.load)  # must keep a reference to this

        if self.image is not None:  # if an image was already loaded
            self.canvas.delete(self.image)  # remove the previous image

        self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)

    def histogram(self):
        hst = self.load.histogram()
        Red = hst[0:256]  # indicates Red
        Green = hst[256:512]  # indicated Green
        Blue = hst[512:768]  # indicates Blue
        plt.figure(num='Red')  # plots a figure to display RED Histogram
        for i in range(0, 256):
            plt.bar(i, Red[i], color = '#%02x%02x%02x'%(i,0,0), alpha=0.3)
        plt.figure(num='Green')  # plots a figure to display GREEN Histogram
        for i in range(0, 256):
            plt.bar(i, Green[i], color = '#%02x%02x%02x'%(0,i,0), alpha=0.3)
        plt.figure(num='Blue')  # plots a figure to display BLUE Histogram
        for i in range(0, 256):
            plt.bar(i, Blue[i], color = '#%02x%02x%02x'%(0,0,i), alpha=0.3)
        plt.show()


class RotateWindow:
    def __init__(self, main_window, w_h_array):
        self.main = main_window
        self.window = Toplevel(self.main)
        w, h = w_h_array[0], w_h_array[1]
        self.window.geometry("190x165+{}+{}".format(510 + w, h))
        self.window.title("Degrees number")
        self.window.resizable(False, False)
        v = StringVar()
        degrees = Label(self.window, text="Degrees").pack()
        self.degrees_entry = Entry(self.window, textvariable=v, width=5).pack()
        Button(self.window, text="Submit", command=lambda: self.rotate(v)).pack()


    def rotate(self, degrees):
        self.main.load = self.main.load.rotate(int(degrees.get()))
        w, h = self.main.load.size
        self.main.render = ImageTk.PhotoImage(self.main.load)  # must keep a reference to this

        if self.main.image is not None:  # if an image was already loaded
            self.main.canvas.delete(self.main.image)  # remove the previous image

        self.main.image = self.main.canvas.create_image((w / 2, h / 2), image=self.main.render)

        self.window.destroy()


class ResizeWindow:
    def __init__(self, main_window, w_h_array):
        self.main = main_window
        self.window = Toplevel(self.main)
        w, h = w_h_array[0], w_h_array[1]
        self.window.geometry("190x165+{}+{}".format(510 + w, h))
        self.window.title("Degrees number")
        self.window.resizable(False, False)
        ht = StringVar()
        wt = StringVar()
        height = Label(self.window, text="Height").pack()
        self.height_entry = Entry(self.window, textvariable=ht, width=5).pack()
        width = Label(self.window, text="Width").pack()
        self.width_entry = Entry(self.window, textvariable=wt, width=5).pack()
        Button(self.window, text="Submit", command=lambda: self.resize(wt, ht)).pack()


    def resize(self, width, height):
        self.main.load = self.main.load.resize((int(width.get()), int(height.get())), Image.ANTIALIAS)
        w, h = self.main.load.size
        self.main.render = ImageTk.PhotoImage(self.main.load)  # must keep a reference to this

        if self.main.image is not None:  # if an image was already loaded
            self.main.canvas.delete(self.main.image)  # remove the previous image

        self.main.image = self.main.canvas.create_image((w / 2, h / 2), image=self.main.render)

        root.geometry("%dx%d" % (w, h))

        self.window.destroy()


class ScaleWindow:
    def __init__(self, main_window, w_h_array):
        self.main = main_window
        self.window = Toplevel(self.main)
        w, h = w_h_array[0], w_h_array[1]
        self.window.geometry("190x165+{}+{}".format(510 + w, h))
        self.window.title("Degrees number")
        self.window.resizable(False, False)
        ht = StringVar()
        wt = StringVar()
        height = Label(self.window, text="Height").pack()
        self.height_entry = Entry(self.window, textvariable=ht, width=5).pack()
        width = Label(self.window, text="Width").pack()
        self.width_entry = Entry(self.window, textvariable=wt, width=5).pack()
        Button(self.window, text="Submit", command=lambda: self.scale(wt, ht)).pack()


    def scale(self, width, height):
        w = int(width.get())
        h = int(height.get())
        self.main.load.thumbnail((w, h), Image.ANTIALIAS)
        self.main.render = ImageTk.PhotoImage(self.main.load)  # must keep a reference to this

        if self.main.image is not None:  # if an image was already loaded
            self.main.canvas.delete(self.main.image)  # remove the previous image

        self.main.image = self.main.canvas.create_image((w / 2, h / 2), image=self.main.render)

        root.geometry("%dx%d" % (w, h))

        self.window.destroy()

root = Tk()
root.geometry("%dx%d" % (300, 300))
root.title("Graphical redactor")
app = MainWindow(root)
app.pack(fill=BOTH, expand=1)
root.mainloop()