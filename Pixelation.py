from tkinter import *
from PIL import Image, ImageTk
import time
import random
from InfiniteCanvas import InfiniteCanvas 

#   TODO
#       allow for changing of color generation type
#       re-implement the color-step algorithm
#       reconfigure the background color?



def average(image, x, y, r):
    rkernel, gkernel, bkernel = 0, 0, 0
    rtot, gtot, btot = 0, 0, 0
    for kx in range(x, x + r):
        for ky in range(y, y + r):
            try:
                pixel = image.getpixel((kx, ky))
                if kx >= 0 and ky >= 0:
                    rkernel, gkernel, bkernel = rkernel + pixel[0], gkernel + pixel[1], bkernel + pixel[2]
                    rtot, gtot, btot = rtot + 1, gtot + 1, btot + 1
            except:
                pass
    red = rkernel / rtot if rtot != 0 else 0
    green = gkernel / gtot if gtot != 0 else 0
    blue = bkernel / btot if btot != 0 else 0
    return int(red), int(green), int(blue)
def color_step(image, x, y, pixelSize, toleranceColor, tolerance, toleranceStep, toleranceStepper):
    return
    def decreaseBrightness(color, times):
        red, green, blue = color
        rSubtract, gSubtract, bSubtract = red / toleranceStepper, green / toleranceStepper, blue / toleranceStepper
        red, green, blue = int(red - times * (rSubtract)), int(green - times * (gSubtract)), int(blue - times * (bSubtract))
        return red, green, blue
    avg = average(image, x, y, pixelSize)
    
    color = ''
    avg = (avg[0] + avg[1] + avg[2]) / 3
    for i in range(int(tolerance / toleranceStep)):
        if avg >= tolerance - toleranceStep * i :
            color = decreaseBrightness(toleranceColor, i)
            break
    if color == '':
        color = decreaseBrightness(toleranceColor, toleranceStepper - int((toleranceStepper - (tolerance / toleranceStep)) / 2))
    return color
def inverted(color):
    return 255 - color[0], 255 - color[1], 255 - color[2]

def lego(input_color):
    closest = 100000
    colors = [(0, 175, 77), (0, 190, 211), (181, 28, 125), (59, 24, 13), 
            (24, 158, 159), (0, 108, 183), (252, 195, 158), (175, 116, 70), 
            (255, 205, 3), (221, 26, 33), (221, 196, 142), (21, 21, 21), 
            (0, 57, 94), (160, 161, 159), (150, 117, 180), (0, 146, 71), 
            (222, 139, 95), (255, 245, 121), (72, 158, 206), (204, 225, 151), 
            (246, 173, 205), (154, 202, 60), (230, 237, 207), (103, 130, 151), 
            (148, 126, 95), (166, 83, 84), (0, 163, 218), (120, 191, 234), 
            (251, 171, 24), (233, 93, 162), (188, 166, 208), (193, 228, 218), 
            (249, 108, 98), (245, 125, 32), (100, 103, 101), (105, 46, 20), 
            (127, 19, 27), (244, 244, 244),(130, 131, 83)]
    for color in colors:
        closeness = 0
        red = abs(color[0] - input_color[0])
        green = abs(color[1] - input_color[1])
        blue = abs(color[2] - input_color[2])
        if red > 50:
            red = 1000
        if green > 50:
            green = 1000
        if blue > 50:
            blue = 1000
        closeness = red + green + blue
        if closeness <= closest:
            closest = closeness
            color_return = color
    return color_return[0], color_return[1], color_return[2]

class Config():
    def __init__(self, app, width=500, height=500) -> None:
        self.app = app
        self.tl = Toplevel(master=app.root)
        self.tl.title("Configure")
        self.tl.config(background='#1b1b1b')
        self.tl.geometry(str(width) + 'x' + str(height) + '+900+60')

        self.canvas = Canvas(self.tl, highlightthickness=0, background='#1b1b1b')
        self.canvas.config(height = height / 2+ 1, width = width / 2 + 1)
        self.canvas.pack(fill=BOTH)

        self.canvas2 = Canvas(self.tl, highlightthickness=0, background='black')
        self.canvas2.config(height = height / 2+ 1, width = width / 2+ 1)
        self.canvas2.pack()


        # Some default values for testing
        self.app.image_path = './Resources/moon.jpg'
        self.square = True
        self.distance = 0
        self.size = 10
        self.padding = 1
        self.offset_x, self.offset_y = 0, 0
        self.animate = 'both'
        self.detect_range = -1
        self.detect_offset_x, self.detect_offset_y = 0, 0
        self.estimated_x, self.estimated_y = 0, 0
        self.lego = False

        self.create_buttons()
        self.config_change()
        self.resize()
        self.tl.bind("<space>", self.app.canvas._set_position)



    def create_buttons(self):
        w, h = self.app.width, self.app.height
        label_fg = 'white'
        label_bg='#1b1b1b'
        Label(self.canvas, text="File ", bg=label_bg, fg=label_fg).grid(row=0, column=0, padx=10, sticky='e')
        self.file_sv = StringVar(None, self.app.image_path)
        file_entry = Entry(self.canvas, textvariable=self.file_sv, width=30, relief='flat', highlightbackground='#2b2b2b')
        file_entry.grid(row=0, column=1, columnspan=4)
        file_entry.bind("<Return>", self.resize)


        Label(self.canvas, text="Height ", bg=label_bg, fg=label_fg).grid(row=1, column=0, padx=10, sticky='e')
        self.height_sv = StringVar(None, str(w))
        height_entry = Entry(self.canvas, textvariable=self.height_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        height_entry.grid(row=1, column=1, columnspan=1)
        height_entry.bind("<Return>", self.resize)

        Label(self.canvas, text="Width ", bg=label_bg, fg=label_fg).grid(row=1, column=2, padx=10, sticky='e')
        self.width_sv = StringVar(None, str(h))
        width_entry = Entry(self.canvas, textvariable=self.width_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        width_entry.grid(row=1, column=3, columnspan=1)
        width_entry.bind("<Return>", self.resize)

        Label(self.canvas, text="Press enter to save", background=label_bg, fg=label_fg, foreground=label_fg, font=("Consolas", 11)).grid(row=1, column=5, padx=10, sticky='e')

        Label(self.canvas, text="Dist.", bg=label_bg, fg=label_fg).grid(row=2, column=0, padx=10, sticky='e')
        self.distance_sv = StringVar(None, str(self.distance))
        distance_entry = Entry(self.canvas, textvariable=self.distance_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        distance_entry.grid(row=2, column=1, columnspan=1)
        distance_entry.bind("<Return>", self.config_change)

        Label(self.canvas, text="Pad ", bg=label_bg, fg=label_fg).grid(row=2, column=2, padx=10, sticky='e')
        self.padding_sv = StringVar(None, str(self.padding))
        padding_entry = Entry(self.canvas, textvariable=self.padding_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        padding_entry.grid(row=2, column=3, columnspan=1)
        padding_entry.bind("<Return>", self.config_change)

        Label(self.canvas, text="Size", bg=label_bg, fg=label_fg).grid(row=2, column=4, padx=10, sticky='e')
        self.size_sv = StringVar(None, str(self.size))
        size_entry = Entry(self.canvas, textvariable=self.size_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        size_entry.grid(row=2, column=5, columnspan=1)
        size_entry.bind("<Return>", self.config_change)

        Label(self.canvas, text="X Offset", bg=label_bg, fg=label_fg).grid(row=3, column=0, padx=10, sticky='e')
        self.offset_x_sv = StringVar(None, str(self.offset_x))
        offset_x_entry = Entry(self.canvas, textvariable=self.offset_x_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        offset_x_entry.grid(row=3, column=1, columnspan=1)
        offset_x_entry.bind("<Return>", self.config_change)

        Label(self.canvas, text="Y Offset", bg=label_bg, fg=label_fg).grid(row=3, column=2, padx=10, sticky='e')
        self.offset_y_sv = StringVar(None, str(self.offset_y))
        offset_y_entry = Entry(self.canvas, textvariable=self.offset_y_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        offset_y_entry.grid(row=3, column=3, columnspan=1)
        offset_y_entry.bind("<Return>", self.config_change)


        Label(self.canvas, text="Detect Range", bg=label_bg, fg=label_fg).grid(row=4, column=0, padx=10, sticky='e')
        self.detect_sv = StringVar(None, str(self.detect_range))
        detect_entry = Entry(self.canvas, textvariable=self.detect_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        detect_entry.grid(row=4, column=1, columnspan=1)
        detect_entry.bind("<Return>", self.config_change)
        Label(self.canvas, text="Det. Off. X", bg=label_bg, fg=label_fg).grid(row=4, column=2, padx=10, sticky='e')
        self.detect_offset_x_sv = StringVar(None, str(self.detect_offset_x))
        detect_offset_entry = Entry(self.canvas, textvariable=self.detect_offset_x_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        detect_offset_entry.grid(row=4, column=3, columnspan=1)
        detect_offset_entry.bind("<Return>", self.config_change)
        Label(self.canvas, text="Det. Off. Y", bg=label_bg, fg=label_fg).grid(row=4, column=4, padx=10, sticky='e')
        self.detect_offset_y_sv = StringVar(None, str(self.detect_offset_y))
        detect_offset_entry = Entry(self.canvas, textvariable=self.detect_offset_y_sv, width=4, relief='flat', highlightbackground='#2b2b2b')
        detect_offset_entry.grid(row=4, column=5, columnspan=1)
        detect_offset_entry.bind("<Return>", self.config_change)

        options = [ 'both', 'line', 'none'] 
        Label(self.canvas, text="Animation", bg=label_bg, fg=label_fg).grid(row=5, column=0, padx=10, sticky='e')
        self.animation_sv = StringVar(None, str('none'))
        animation_entry = OptionMenu(self.canvas, self.animation_sv, *options)
        animation_entry.grid(row=5, column=1, columnspan=1)
        animation_entry.bind("<Return>", self.config_change)

        self.square_label = Label(self.canvas, text="[X]/( )", bg=label_bg, fg=label_fg)
        self.square_label.grid(row=7, column=0, sticky='e')
        self.square_button = Button(self.canvas, command=self.toggle_square, relief='flat', background=label_bg, fg=label_fg, width=1)
        self.square_button.grid(row=7, column=1)

        self.lego_label = Label(self.canvas, text="Lego Colors [ ]", bg=label_bg, fg=label_fg)
        self.lego_label.grid(row=8, column=0, sticky='e')
        self.lego_button = Button(self.canvas, command=self.toggle_lego, relief='flat', background=label_bg, fg=label_fg, width=1)
        self.lego_button.grid(row=8, column=1)

        Label(self.canvas, text="Generate!", bg=label_bg, fg=label_fg).grid(row=10, column=0, sticky='e')
        self.generate_button = Button(self.canvas, command=self.generate, relief='flat', background=label_bg, fg=label_fg, width=1)
        self.generate_button.grid(row=10, column=1)

        Label(self.canvas, text="Toggle Pixels", bg=label_bg, fg=label_fg).grid(row=10, column=2, sticky='e')
        self.generate_button = Button(self.canvas, command=self.app.toggle_pixels, relief='flat', background=label_bg, fg=label_fg, width=1)
        self.generate_button.grid(row=10, column=3)

        Label(self.canvas, text="Toggle Image", bg=label_bg, fg=label_fg).grid(row=10, column=4, sticky='e')
        self.generate_button = Button(self.canvas, command=self.app.toggle_image, relief='flat', background=label_bg, fg=label_fg, width=1)
        self.generate_button.grid(row=10, column=5)


        self.est_label_x = Label(self.canvas, text=str("Pixels X: " + str(int(self.estimated_x))), background=label_bg, fg=label_fg, foreground=label_fg, font=("Consolas", 11))
        self.est_label_x.grid(row=11, column=0, columnspan=2, padx=10, sticky='e')
        self.est_label_y = Label(self.canvas, text=str("Pixels Y: " + str(int(self.estimated_y))), background=label_bg, fg=label_fg, foreground=label_fg, font=("Consolas", 11))
        self.est_label_y.grid(row=11, column=1, columnspan=2, padx=10, sticky='e')


    def config_change(self, event=None):
        self.distance = int(self.distance_sv.get())
        self.padding = int(self.padding_sv.get())
        self.size = int(self.size_sv.get())
        self.offset_x = int(self.offset_x_sv.get())
        self.offset_y = int(self.offset_y_sv.get())
        self.detect_range = int(self.detect_sv.get())
        self.detect_offset_x = int(self.detect_offset_x_sv.get())
        self.detect_offset_y = int(self.detect_offset_y_sv.get())
        self.animate = self.animation_sv.get()
        self.draw_sample()

    def toggle_square(self):
        self.square = not self.square
        if self.square:
            self.square_label.config(text="[X]/( )")
        else:
            self.square_label.config(text="[ ]/(X)")
        self.draw_sample()

    def toggle_lego(self):
        self.lego = not self.lego
        if self.lego:
            self.lego_label.config(text="Lego Colors [X]")
        else:
            self.lego_label.config(text="Lego Colors [ ]")
        self.draw_sample()

    def resize(self, event=None):
        self.app.image_path = self.file_sv.get()
        if self.app.image_path != '':
            height, width = int(self.height_sv.get()), int(self.width_sv.get())
            self.app.image_path = self.file_sv.get()
            self.app.resize_image(width, height)
            if height == 0 or width == 0:
                width, height = self.app.image.size
            self.width_sv.set(width)
            self.height_sv.set(height)
            image = Image.open(self.file_sv.get())
            image = image.resize((width, height))
            self.tk_image = ImageTk.PhotoImage(image)
            self.canvasImage = self.canvas2.create_image(width / 2, height / 2, image=self.tk_image)
        self.draw_sample()

    def generate(self):
        self.config_change()
        self.resize()
        self.app.pixelate(self.offset_x, self.offset_y, self.distance, self.padding, self.size, self.square, self.detect_range, self.detect_offset_x, self.detect_offset_y, self.animate, self.lego)


    def draw_sample(self):
        for item in self.canvas2.find_withtag('nonimage'):
            self.canvas2.delete(item)
        self.canvas2.update()

        self.estimated_x = int(self.height_sv.get()) / (self.size + self.distance)
        self.estimated_y = int(self.width_sv.get()) / (self.size + self.distance)
        self.est_label_x.config(text='Pixels X:' + str(int(self.estimated_x)))
        self.est_label_y.config(text='Pixels Y:' + str(int(self.estimated_y)))
        if self.detect_range == -1:
            self.detect_range = self.size
        for y in range(0, self.canvas2.winfo_height(), self.size + self.distance):
            for x in range(0, self.canvas2.winfo_width(), self.size + self.distance):
                array_4 = [x + self.padding + self.offset_x, y + self.padding + self.offset_y, 
                           x + self.size - self.padding  + self.offset_x, y + self.size - self.padding  + self.offset_y]
                detect_array_4 = [x + self.detect_range + self.detect_offset_x + self.offset_x, y + self.detect_range + self.detect_offset_y + self.offset_y, 
                           x + self.size - self.detect_range  + self.detect_offset_x + self.offset_x, y + self.size - self.detect_range  + self.detect_offset_y + self.offset_y]
                self.canvas2.create_rectangle(detect_array_4, fill='', outline='red', tags='nonimage')
                if self.square:
                    self.canvas2.create_rectangle(array_4, fill='white', outline='black', tags='nonimage')
                else:
                    self.canvas2.create_oval(array_4, fill='white', outline='black', tags='nonimage')

class ScrollableCanvas(InfiniteCanvas):
    def _scroll(self, event):
        self.master.title('Press space to return to origin')
        super()._scroll(event)
    def _set_position(self, event):
        self.master.title('Image')
        super()._set_position(event)

class App():
    def __init__(self, image_path='') -> None:
        self.root = Tk()
        self.root.title("Image")
        self.root.resizable(False, False)
        self.root.geometry('500x500')

        self.canvas = ScrollableCanvas(self.root, highlightthickness=0, background='#2b2b2b')
        self.canvas.pack(expand=1, fill=BOTH)

        self.pixels = []
        self.width, self.height = 0, 0
        self.image_path = image_path


    def resize_image(self, width=0, height=0):
        self.root.resizable(True, True)
        self.image = Image.open(self.image_path)
        if height == 0 or width == 0:
            width, height = self.image.size
        self.image = self.image.resize((width, height))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas_image = self.canvas.create_image(width/2, height/2, image=self.tk_image)
        self.root.geometry(str(min(width, 1400)) + 'x' + str(min(height, 850)))
        self.width, self.height = width, height
        self.root.update()
        self.root.resizable(False, False)
    def toggle_image(self, event=None):
        if self.canvas.itemcget(self.canvas_image, 'state') == 'hidden':
            self.canvas.itemconfig(self.canvas_image, state = 'normal')
        else:
            self.canvas.itemconfig(self.canvas_image, state='hidden')
    def toggle_pixels(self, event=None):
        if len(self.pixels) > 0:
            if (self.canvas.itemcget(self.pixels[0], 'state') == 'hidden'):
                for pixel in self.pixels:
                    self.canvas.itemconfig(pixel, state = 'normal')
            else:
                for pixel in self.pixels:
                    self.canvas.itemconfig(pixel, state = 'hidden')
    def clearPixels(self, event=None):
        if len(self.pixels) > 0:
            for pixel in self.pixels:
                self.canvas.delete(pixel)
            self.pixels = []
    def check(self, event, num):
        if self.canvas.itemcget(num, 'outline') == 'red':
            self.canvas.itemconfig(num, outline='', width=1)
        else:
            self.canvas.itemconfig(num, outline='red', width=2)
    def pixelate(self, offset_x, offset_y, distance, padding, size, square, detect_range, detect_offset_x, detect_offset_y, animate, lego_on):
        for item in self.pixels:
            self.canvas.delete(item)
        self.canvas.update()
        for y in range(offset_y, self.height, size + distance):
            if animate == 'both' or animate == 'line':
                self.canvas.update()
            for x in range(offset_x, self.width, size + distance):
                if animate == 'both':
                    self.canvas.update()


                color = average(self.image, x + detect_offset_x, y + detect_offset_y, size if detect_range == -1 else detect_range)
                if lego_on:
                    color = lego(color)

                color = '#%02x%02x%02x' % (color[0], color[1], color[2])
                array_4 = [x + padding + offset_x, y + padding + offset_y, 
                           x + size - padding  + offset_x, y + size - padding  + offset_y]
                if square:
                    pixel = self.canvas.create_rectangle(array_4, fill=color, outline='')
                else:
                    pixel = self.canvas.create_oval(array_4, fill=color, outline='')
                self.pixels.append(pixel)
                self.canvas.tag_bind(pixel, "<Button-1>", lambda event, num=pixel: self.check(event, num))

                

    def run(self):
        self.root.mainloop()



if __name__ == "__main__":

    app = App()
    config = Config(app)
    app.run()