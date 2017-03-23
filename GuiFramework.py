import tkinter as tk
from PIL import ImageTk, Image
from win32api import GetSystemMetrics

import sys

class Step():

   def __init__(self, text, weight, ingredient ):
       self.text = text
       self.weight = weight
       self.ingredient = ingredient

TITLE_FONT = ("Helvetica", 18, "bold")
##RecipeList
recipelist = [("Pancakes", "Required Ingredients: \n 1 1/2 cups of flour \n 3 1/2 teaspoons of baking powder, 1 teaspoon of salt \n 1 tablespoon of white sugar\n 1 1/4 cups of milk\n 1 egg \n 3 tablespoons of melted butter", Step("Place bowl on scale and zero",0,"N/A")),
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

##Screen Dimensions
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

def startRecipe(controller):
    controller.show_frame("Recipe")

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

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

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
        button2 = tk.Button(self, text="Settings", command=lambda: startRecipe(controller))
        button2img = ImageTk.PhotoImage(file="assets/settings.png")
        button2.config(image=button2img)
        button2.image = button2img
        button1.pack()
        button2.pack()

class Recipes(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Recipes")
        label.pack(side="top", fill="x", pady=10)
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT)
        listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        for r in recipelist:
            listbox.insert(tk.END, r[0])
        listbox.bind('<<ListboxSelect>>', self.recipeSelect)
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

    def recipeSelect(self, event):
        recipePage = self.controller.get_page("Recipe")
        w = event.widget
        index = int(w.curselection()[0])
        value = recipelist[(index)][0]
        recipePage.currentRecipe.set(value)
        #print(recipePage.currentRecipe.get())
        self.update_idletasks()
        #self.controller.show_frame("Recipe")

class Recipe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.currentRecipe = tk.StringVar()
        ##get width and height
        global width
        global height
        ##Instruction
        instructionlabel = tk.Label(self, textvariable = self.currentRecipe, font=TITLE_FONT)
        instructionlabel.pack(anchor="center", fill="x", pady=height/7.5)
        ##HomeButton
        homebutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        homeimage = ImageTk.PhotoImage(file="assets/home.png")
        homebutton.config(image=homeimage)
        homebutton.image = homeimage
        homebutton.config(height=height / 10, width=width/3, bg="#3A5199")
        homebutton.place(rely=0, relx=0, x=0, y=0, anchor='nw')
        ##Recipesbutton
        recipesbutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        recipesimage = ImageTk.PhotoImage(file="assets/home.png")
        recipesbutton.config(image=recipesimage)
        recipesbutton.image = recipesimage
        recipesbutton.config(height=height / 10, width=width / 3, bg="#3A5199")
        recipesbutton.place(rely=0, relx=0.5, x=0, y=0, anchor='n')
        ##settingsbutton
        settingsbutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        settingsimage = ImageTk.PhotoImage(file="assets/settings.png")
        settingsbutton.config(image=settingsimage)
        settingsbutton.image = settingsimage
        settingsbutton.config(height=height / 10, width=width / 3, bg="#3A5199")
        settingsbutton.place(rely=0, relx=1, x=0, y=0, anchor='ne')
        ##Back and Next buttons
        nextbutton = tk.Button(self, text="Home", borderwidth=5, command=lambda: controller.show_frame("HomePage"))
        nextimage = ImageTk.PhotoImage(file="assets/home.png")
        nextbutton.config(image=nextimage)
        nextbutton.image = nextimage
        nextbutton.config(height = height/10, width=width/2, bg="#2F2E33")
        nextbutton.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
        backbutton = tk.Button(self, text="Home", borderwidth=5, command=lambda: controller.show_frame("HomePage"))
        backimage = ImageTk.PhotoImage(file="assets/home.png")
        backbutton.config(image=backimage)
        backbutton.image = backimage
        backbutton.config(height=height / 10, width=width / 2, bg="#2F2E33")
        backbutton.place(rely=1.0, relx=0, x=0, y=0, anchor='sw')







if __name__ == "__main__":
    app = ScaleApp()
    app.mainloop()