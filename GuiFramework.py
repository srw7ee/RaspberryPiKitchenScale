##credit to http://icons8.com(egg.png) and https://icons8.com/ (flour.png, oil.png) for the icons
import tkinter as tk
from PIL import ImageTk, Image
from win32api import GetSystemMetrics
from ScaleMethods import getWeightInGrams

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

   def getIngredient(self):
       return self.ingredient

TITLE_FONT = ("Helvetica", 18, "bold")
##RecipeList
recipelist = [("Pancakes", "Required Ingredients: \n 1 1/2 cups of flour \n 3 1/2 teaspoons of baking powder, 1 teaspoon"
                           " of salt \n 1 tablespoon of white sugar\n 1 1/4 cups of milk\n 1 egg \n 3 tablespoons of "
                           "melted butter", Step("Place bowl on scale",-1,"oil"),
                            Step("Add 1 1/2 cups of sifted flour",185,"flour"),
                            Step("Add 3 1/2 teaspoons of baking powder",14,"flour"),
                            Step("Add 1 teaspoon of salt",4,"flour"),
                            Step("Add 1 tablespoon of white sugar",12,"flour"),
                            Step("Make a well in the center and add pour in 1 1/4 cups of milk",306,"flour"),
                            Step("Add 1 egg",-1,"flour"), Step("Add 3 tablespoons of melted butter",42,"flour"),
                            Step("Remove from scale and mix until smooth",-1,"flour"),
                            Step("Heat and oil cooking surface to medium high",-1,"flour"),
                            Step("Add 1/4 a cup of batter and brown on each side",-1,"flour"),
                            Step("Serve hot",-1,"flour")),
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
        self.progress_function()
        self.mainloop()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]

    def progress_function(self):
        print(getWeightInGrams())
        recipePage = self.get_page("Recipe")
        recipePage.progress_function()

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
        recipePage.index = index
        recipePage.max = recipelist[(index)][2].getWeight()
        imageName = "assets/"+ recipelist[(index)][2].getIngredient()+".png"
        recipePage.ingredientimage = tk.PhotoImage(file=imageName)
        global width
        while (recipePage.ingredientimage.width() > width / 3):
            recipePage.ingredientimage = recipePage.ingredientimage.subsample(2, 2)
        recipePage.imagePanel.configure(image=recipePage.ingredientimage)
        recipePage.update_idletasks()
        #self.controller.show_frame("Recipe")

class Recipe(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.currentStep = tk.StringVar()
        self.recipe = 0
        self.index = 0
        self.max = 1
        ##get width and height
        global width
        global height
        ##IngredientImage
        self.ingredientimage = tk.PhotoImage(file="assets/egg.png")
        while(self.ingredientimage.width() > width/3):
            self.ingredientimage = self.ingredientimage.subsample(2, 2)
        self.imagePanel = tk.Label(self, image = self.ingredientimage)
        self.imagePanel.place(rely=0, relx=0, x=width / 6, y=height / 2, anchor="center")
        ##Instruction
        self.instructionlabel = tk.Label(self, textvariable = self.currentStep, font=TITLE_FONT,  wraplength=width/3 )
        self.instructionlabel.place(rely=0, relx=0, x=width/2, y=height/3, anchor="center")
        ##Progress Percentage
        self.progress_var = tk.StringVar()
        self.progress_var.set(123)
        self.progresslabel = tk.Label(self, textvariable=self.progress_var, font=TITLE_FONT, wraplength=width/3)
        self.progresslabel.config(font=("Helvetica", 44, "bold"))
        self.progresslabel.place(rely=0, relx=0, x=width*5/6, y=height/2, anchor="center")
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
        ##Next buttons
        nextbutton = tk.Button(self, text="Home", borderwidth=4, command=lambda: self.nextStep())
        nextimage = tk.PhotoImage(file="assets/NextArrowWhite.png")
        nextimage = nextimage.subsample(2, 2)
        nextbutton.config(image=nextimage)
        nextbutton.image = nextimage
        nextbutton.config(height = height/10, width=width/2, bg="#2F2E33")
        nextbutton.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
        ##Back Button
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
            self.max = recipelist[(self.recipe)][self.index+2].getWeight()
            self.update_idletasks()
            self.controller.show_frame("HomePage")
        else:
            self.index += 1
            step = recipelist[(self.recipe)][self.index+2]
            self.max = step.getWeight()
            self.currentStep.set(step.getText())
            imageName = "assets/" + step.getIngredient() + ".png"
            self.ingredientimage = tk.PhotoImage(file=imageName)
            global width
            while (self.ingredientimage.width() > width / 3):
                self.ingredientimage = self.ingredientimage.subsample(2, 2)
            self.imagePanel.configure(image=self.ingredientimage)
            # print(recipePage.currentRecipe.get())
            self.update_idletasks()
            # self.controller.show_frame("Recipe")

    def prevStep(self):
        if(self.index > 0):
            self.index -= 1
            step = recipelist[(self.recipe)][self.index + 2]
            self.currentStep.set(step.getText())
            self.max = step.getWeight()
            imageName = "assets/" + step.getIngredient() + ".png"
            #print(imageName)
            self.ingredientimage = tk.PhotoImage(file=imageName)
            global width
            while (self.ingredientimage.width() > width / 3):
                self.ingredientimage = self.ingredientimage.subsample(2, 2)
            self.imagePanel.configure(image=self.ingredientimage)
            self.update_idletasks()
            # self.controller.show_frame("Recipe")

    def progress_function(self):
        #print(getWeightInGrams())
        curr = getWeightInGrams()
        #print(round(curr / self.max, 2)*100)
        if((self.max is 1 or self.max is -1) and (curr>abs(self.max))):
            self.progress_var.set("100")
        elif((round(curr / self.max, 2)*100)>100):
            self.progress_var.set("100")
        else:
            self.progress_var.set(abs(round(round(curr / self.max, 2)*100,2)))
            self.update_idletasks()
        self.controller.after(100, self.controller.progress_function)


if __name__ == "__main__":
    app = ScaleApp()
