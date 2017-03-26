##credit to http://icons8.com(egg.png) and https://icons8.com/ (flour.png, oil.png) for the icons
import tkinter as tk
from PIL import ImageTk, Image
import subprocess
#from win32api import GetSystemMetrics
#from ScaleMethods import getWeightInGrams

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
NORMAL_FONT = ("Helvetica", 12)
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
output = subprocess.Popen('xrandr | grep \* | cut -d" " -f4', shell=True, stdout=subprocess.PIPE).communicate()[0]
width = 480 #GetSystemMetrics(0)
height = 320 #GetSystemMetrics(1)
print(output)
print(height)

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
        self.geometry('{}x{}'.format(width, height))
        #self.attributes("-fullscreen", True)
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
        print(0)#getWeightInGrams())
        recipePage = self.get_page("Recipe")
        recipePage.progress_function()

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        global width, height
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome!", font=TITLE_FONT)
        #label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Test", command=lambda: controller.show_frame("Recipes"))
        image = ImageTk.PhotoImage(file="assets/book.png")
        button1.config(image=image, width=width, height=2*height/3, bg="#006400")
        button1.image = image
        button2 = tk.Button(self, text="Settings", command=lambda: startRecipe(controller))
        button2img = ImageTk.PhotoImage(file="assets/settings.png")
        button2.config(image=button2img, bg="#2F2E33", width=width, height=height/3)
        button2.image = button2img
        button1.pack()
        button2.pack()

class Recipes(tk.Frame):

    def __init__(self, parent, controller):
        global width, height
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.homebutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        self.homeimage = Image.open("assets/home.png")
        self.homeimage = self.homeimage.resize((int(self.homeimage.size[0]/2), int(self.homeimage.size[1]/2)), Image.ANTIALIAS)
        self.homeimage = ImageTk.PhotoImage(self.homeimage)
        self.homebutton.config(image=self.homeimage)
        self.homebutton.image = self.homeimage
        self.homebutton.config(height=height / 10, width=width/2, bg="#3A5199")
        self.homebutton.place(rely=0, relx=0, x=0, y=0, anchor='nw')
        #Settings icon
        self.settingsbutton = tk.Button(self, text="Settings", command=lambda: controller.show_frame("HomePage"))
        self.settingsimage = Image.open("assets/settings.png")
        self.settingsimage = self.settingsimage.resize((int(self.settingsimage.size[0]/2), int(self.settingsimage.size[1]/2)), Image.ANTIALIAS)
        self.settingsimage = ImageTk.PhotoImage(self.settingsimage)
        self.settingsbutton.config(image=self.settingsimage)
        self.settingsbutton.image = self.settingsimage
        self.settingsbutton.config(height=height / 10, width=width/2, bg="#3A5199")
        self.settingsbutton.place(rely=0, relx=1, x=0, y=0, anchor='ne')
        scrollbar = tk.Scrollbar(self)
        #scrollbar.pack(side=tk.RIGHT)
        listbox = tk.Listbox(self, yscrollcommand=scrollbar.set, width=int(width/15))
        for r in recipelist:
            listbox.insert(tk.END, r[0])
        #listbox.config(width=int(0.8*width), height=int(0.8*height))
        listbox.bind('<<ListboxSelect>>', self.recipeSelect)
        listbox.place(rely=.5, relx=0, x=0, y=0, anchor='w')
        self.ingredientlabel = tk.Label(self, text="Select a Recipe", font=NORMAL_FONT, wraplength=width/2)
        self.ingredientlabel.place(rely=0, relx=0, x=width*3/4, y=height/2, anchor="center")
        scrollbar.config(command=listbox.yview)
        gobutton = tk.Button(self, text="Go", command=lambda: controller.show_frame("Recipe"))
        gobutton.config(width=width, bg="#006400")
        goimage = Image.open("assets/go.png")
        goimage = ImageTk.PhotoImage(goimage)
        gobutton.config(image=goimage)
        gobutton.image=goimage
        gobutton.place(rely=0, relx=0, x=width/2, y=height-32, anchor='center')

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
        recipePage.ingredientimage = Image.open("assets/settings.png")
        recipePage.ingredientimage = ImageTk.PhotoImage(recipePage.ingredientimage)
        self.ingredientlabel.config(text=recipelist[index][1])
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
        self.ingredientimage = Image.open("assets/egg.png")
        while(self.ingredientimage.width > width/3):
            self.ingredientimage = self.ingredientimage.resize((int(self.ingredientimage.size[0]/2), int(self.ingredientimage.size[1]/2)), Image.ANTIALIAS)
        self.ingredientimage = ImageTk.PhotoImage(self.ingredientimage)
        self.imagePanel = tk.Label(self, image=self.ingredientimage)
        self.imagePanel.image=self.ingredientimage
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
        self.homeimage = Image.open("assets/home.png")
        self.homeimage = self.homeimage.resize((int(self.homeimage.size[0]/2), int(self.homeimage.size[1]/2)), Image.ANTIALIAS)
        self.homeimage = ImageTk.PhotoImage(self.homeimage)
        self.homebutton.config(image=self.homeimage)
        self.homebutton.image = self.homeimage
        self.homebutton.config(height=height / 10, width=width/3, bg="#3A5199")
        self.homebutton.place(rely=0, relx=0, x=0, y=0, anchor='nw')
        ##Recipesbutton
        self.recipesbutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("Recipes"))
        self.recipesimage = Image.open("assets/book.png")
        self.recipesimage = self.recipesimage.resize((int(self.recipesimage.size[0]/2), int(self.recipesimage.size[1]/2)), Image.ANTIALIAS)
        self.recipesimage = ImageTk.PhotoImage(self.recipesimage)
        self.recipesbutton.config(image=self.recipesimage)
        self.recipesbutton.image = self.recipesimage
        self.recipesbutton.config(height=height / 10, width=width / 3, bg="#3A5199")
        self.recipesbutton.place(rely=0, relx=0.5, x=0, y=0, anchor='n')
        ##settingsbutton
        self.settingsbutton = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        self.settingsimage = Image.open("assets/settings.png")
        self.settingsimage = self.settingsimage.resize((int(self.settingsimage.size[0]/2), int(self.settingsimage.size[1]/2)), Image.ANTIALIAS)
        self.settingsimage = ImageTk.PhotoImage(self.settingsimage)
        self.settingsbutton.config(image=self.settingsimage)
        self.settingsbutton.image = self.settingsimage
        self.settingsbutton.config(height=height / 10, width=width / 3, bg="#3A5199")
        self.settingsbutton.place(rely=0, relx=1, x=0, y=0, anchor='ne')
        ##Next buttons
        self.nextbutton = tk.Button(self, text="Home", borderwidth=4, command=lambda: self.nextStep())
        self.nextimage = Image.open("assets/NextArrowWhite.png")
        self.nextimage = self.nextimage.resize((int(self.nextimage.size[0]/4), int(self.nextimage.size[1]/4)), Image.ANTIALIAS)
        self.nextimage = ImageTk.PhotoImage(self.nextimage)
        self.nextbutton.config(image=self.nextimage)
        self.nextbutton.image = self.nextimage
        self.nextbutton.config(height = height/10, width=width/2, bg="#2F2E33")
        self.nextbutton.place(rely=1.0, relx=1.0, x=0, y=0, anchor='se')
        ##Back Button
        self.backbutton = tk.Button(self, text="Home", borderwidth=4, command=lambda: self.prevStep())
        self.backimage = Image.open("assets/BackArrowWhite.png")
        self.backimage = self.backimage.resize((int(self.backimage.size[0]/4), int(self.backimage.size[1]/4)), Image.ANTIALIAS)
        self.backimage = ImageTk.PhotoImage(self.backimage)
        self.backbutton.config(image=self.backimage)
        self.backbutton.image = self.backimage
        self.backbutton.config(height=height / 10, width=width / 2, bg="#2F2E33")
        self.backbutton.place(rely=1.0, relx=0, x=0, y=0, anchor='sw')

    def nextStep(self):
        global width
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
            self.ingredientimage = Image.open(imageName)
            while(self.ingredientimage.width > width/3):
                self.ingredientimage = self.ingredientimage.resize((int(self.ingredientimage.size[0]/2), int(self.ingredientimage.size[1]/2)), Image.ANTIALIAS)
            self.ingredientimage = ImageTk.PhotoImage(self.ingredientimage)
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
            self.ingredientimage = Image.open(imageName)
            while(self.ingredientimage.width > width/3):
                self.ingredientimage = self.ingredientimage.resize((int(self.ingredientimage.size[0]/2), int(self.ingredientimage.size[1]/2)), Image.ANTIALIAS)
            self.ingredientimage = ImageTk.PhotoImage(self.ingredientimage)
            self.imagePanel.configure(image=self.ingredientimage)
            self.update_idletasks()
            # self.controller.show_frame("Recipe")

    def progress_function(self):
        #print(getWeightInGrams())
        curr = 0 #getWeightInGrams()
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
