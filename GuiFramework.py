import tkinter as tk
from PIL import ImageTk, Image

import sys

TITLE_FONT = ("Helvetica", 18, "bold")
recipelist = [("Beef Wellington", "HomePage"),
              ("Caramel", "HomePage"),
              ("Chardonnay", "HomePage"),
              ("Cheese Pizza", "HomePage"),
              ("Chicken Alfredo", "HomePage"),
              ("Foie Gras", "HomePage"),
              ("French Fries", "HomePage"),
              ("Hot Water", "HomePage"),
              ("Ice Water", "HomePage"),
              ("Vanilla Pudding", "HomePage")
]

class ScaleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #container for all frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #stack frames in the container
        self.frames = {}
        for F in (HomePage, Recipes, Recipe):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("HomePage")
        self.attributes("-fullscreen", True)
        self.bind('<Escape>',sys.exit)


        #self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth()-3, self.winfo_screenheight()-3))

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome!", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Test", command=lambda: controller.show_frame("Recipes"))
        image = ImageTk.PhotoImage(file="assets/recipes.png")
        button1.config(image=image)
        button1.image = image
        button2 = tk.Button(self, text="Settings", command=lambda: controller.show_frame("Recipe"))
        button2img = ImageTk.PhotoImage(file="assets/settings.png")
        button2.config(image=button2img)
        button2.image = button2img
        button1.pack()
        button2.pack()


class Recipes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Recipes", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT)
        listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        for r in recipelist:
            listbox.insert(tk.END, r[0])
        listbox.pack()
        scrollbar.config(command=listbox.yview)
        homebutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        homeimage = ImageTk.PhotoImage(file="assets/home.png")
        homebutton.config(image=homeimage)
        homebutton.image=homeimage
        homebutton.pack(side="left", padx=10)
        gobutton = tk.Button(self, text="Go", command=lambda: controller.show_frame("Recipe"))
        goimage = ImageTk.PhotoImage(file="assets/go.png")
        gobutton.config(image=goimage)
        gobutton.image=goimage
        gobutton.pack(side="right", padx=10)


class Recipe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("HomePage"))
        button.pack()

class Step():

    def _init__(self, weigh, title, ):
        weigh



if __name__ == "__main__":
    app = ScaleApp()
    app.mainloop()