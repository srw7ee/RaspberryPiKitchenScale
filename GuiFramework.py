import tkinter as tk
from PIL import ImageTk, Image
from win32api import GetSystemMetrics

import sys

class Step():

   def __init__(self, text, weight, ingredient ):
       self.text = text
       self.weight = weight
       self.ingredient = ingredient

   def getText(self):
       return self.text
   def getWeight(self):
       return self.weight

TITLE_FONT = ("Helvetica", 18, "bold")
##RecipeList
recipelist = [("Pancakes", "Required Ingredients: \n 1 1/2 cups of flour \n 3 1/2 teaspoons of baking powder, 1 teaspoon"
                           " of salt \n 1 tablespoon of white sugar\n 1 1/4 cups of milk\n 1 egg \n 3 tablespoons of "
                           "melted butter", Step("Place bowl on scale and zero",0,"N/A"), Step("Step2",0,"N/A")),
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

    ##have to have it update current page and next page with first step in recipe
    def recipeSelect(self, event):
        recipePage = self.controller.get_page("Recipe")
        w = event.widget
        index = int(w.curselection()[0])
        value = recipelist[(index)][2].getText()
        recipePage.currentStep.set(value)
        recipePage.recipe = index
        #print(recipePage.currentStep.get())
        self.update_idletasks()
        #self.controller.show_frame("Recipe")

class Recipe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.currentStep = tk.StringVar()
        self.recipe = 0
        self.index = 0
        ##get width and height
        global width
        global height
        ##Instruction
        self.instructionlabel = tk.Label(self, textvariable = self.currentStep, font=TITLE_FONT,  wraplength=width*.8 )
        self.instructionlabel.pack(anchor="w", fill="x", pady=height/5)
        ##HomeButton
        self.homebutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        self.homeimage = ImageTk.PhotoImage(file="assets/home.png")
        self.homebutton.config(image=self.homeimage)
        self.homebutton.image = self.homeimage
        self.homebutton.config(height=height / 10, width=width/3, bg="#3A5199")
        self.homebutton.place(rely=0, relx=0, x=0, y=0, anchor='nw')
        ##Recipesbutton
        self.recipesbutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("Recipes"))
        self.recipesimage = tk.PhotoImage(file="assets/Book.png")
        self.recipesimage = self.recipesimage.subsample(2, 2)
        self.recipesbutton.config(image=self.recipesimage)
        self.recipesbutton.image = self.recipesimage
        self.recipesbutton.config(height=height / 10, width=width / 3, bg="#3A5199")
        self.recipesbutton.place(rely=0, relx=0.5, x=0, y=0, anchor='n')
        ##settingsbutton
        settingsbutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        settingsimage = tk.PhotoImage(file="assets/settings.png")
        #settingsimage = settingsimage.subsample(2, 2)
        settingsbutton.config(image=settingsimage)
        settingsbutton.image = settingsimage
        settingsbutton.config(height=height / 10, width=width / 3, bg="#3A5199")
        settingsbutton.place(rely=0, relx=1, x=0, y=0, anchor='ne')
        ##Back and Next buttons
        nextbutton = tk.Button(self, text="Home", borderwidth=4, command=lambda: self.nextStep())
        nextimage = tk.PhotoImage(file="assets/NextArrowWhite.png")
        nextimage = nextimage.subsample(2, 2)
        nextbutton.config(image=nextimage)
        nextbutton.image = nextimage
        nextbutton.config(height = height/10, width=width/2, bg="#2F2E33")
        nextbutton.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
        self.backbutton = tk.Button(self, text="Home", borderwidth=4, command=lambda: self.prevStep())
        backimage = tk.PhotoImage(file="assets/BackArrowWhite.png")
        backimage = backimage.subsample(2, 2)
        self.backbutton.config(image=backimage)
        self.backbutton.image = backimage
        self.backbutton.config(height=height / 10, width=width / 2, bg="#2F2E33")
        self.backbutton.place(rely=1.0, relx=0, x=0, y=0, anchor='sw')

    def nextStep(self):
        if(len(recipelist[(self.recipe)]) < self.index+4):
            self.index = 0
            self.currentStep.set(recipelist[(self.recipe)][self.index+2].getText())
            self.update_idletasks()
            self.controller.show_frame("HomePage")
        else:
            self.index += 1
            step = recipelist[(self.recipe)][self.index+2].getText()
            self.currentStep.set(step)
            # print(recipePage.currentRecipe.get())
            self.update_idletasks()
            # self.controller.show_frame("Recipe")

    def prevStep(self):
        if(self.index > 0):
            self.index -= 1
            step = recipelist[(self.recipe)][self.index + 2].getText()
            self.currentStep.set(step)
            self.update_idletasks()
            # self.controller.show_frame("Recipe")


if __name__ == "__main__":
    app = ScaleApp()
    app.mainloop()