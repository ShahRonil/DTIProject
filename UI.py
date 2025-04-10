from tkinter import *
from tkinter import messagebox
import requests
import PIL as p
import PIL.ImageTk as ptk
from io import BytesIO
from datetime import datetime

root = Tk()
root.title("www.BookVerse.com")
root.geometry("1360x1000")

# Images taken from URL
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        return p.Image.open(img_data)
    except requests.RequestException as e:
        print(f"Error fetching image from {url}: {e}")
        return None
    except Exception as e:
        print(f"Error loading image from {url}: {e}")
        return None

# Load images from URLs
def load_images():
    urls = {
        "logo": "https://catalogue.alankarpublication.com/assets/images/gif/1481.gif",
        "large_logo": "https://png.pngtree.com/png-clipart/20230805/original/pngtree-stack-of-books-vintage-illustration-png-image_9418602.png",
        "horror": [
            "https://tse4.mm.bing.net/th?id=OIP.v42yvTWF0czpy1hR2lR3dQAAAA&pid=Api&P=0&h=180",
            "https://tse4.mm.bing.net/th?id=OIP.v42yvTWF0czpy1hR2lR3dQAAAA&pid=Api&P=0&h=180",
            "https://tse4.mm.bing.net/th?id=OIP.v42yvTWF0czpy1hR2lR3dQAAAA&pid=Api&P=0&h=180"
        ],
        "kids": [
            "https://tse3.mm.bing.net/th?id=OIP.SFjqrqjXhps0uwxGVok68gAAAA&pid=Api&P=0&h=180",
            "https://tse3.mm.bing.net/th?id=OIP.SFjqrqjXhps0uwxGVok68gAAAA&pid=Api&P=0&h=180",
            "https://tse3.mm.bing.net/th?id=OIP.SFjqrqjXhps0uwxGVok68gAAAA&pid=Api&P=0&h=180"
        ],
        "mystery": [
            "https://images-na.ssl-images-amazon.com/images/I/71xrhE-8SyL._AC_UL160_SR160,160_.jpg",
            "https://images-na.ssl-images-amazon.com/images/I/71xrhE-8SyL._AC_UL160_SR160,160_.jpg",
            "https://images-na.ssl-images-amazon.com/images/I/71xrhE-8SyL._AC_UL160_SR160,160_.jpg"
        ],
        "humour": [
            "https://i.pinimg.com/originals/e0/77/28/e07728e00b6587c07fc779acdf50342d.jpg",
            "https://i.pinimg.com/originals/e0/77/28/e07728e00b6587c07fc779acdf50342d.jpg",
            "https://i.pinimg.com/originals/e0/77/28/e07728e00b6587c07fc779acdf50342d.jpg"
        ]
    }

    images = {}
    for key, url in urls.items():
        if isinstance(url, list):
            images[key] = []
            for u in url:
                image = load_image_from_url(u)
                if image is not None:
                    images[key].append(ptk.PhotoImage(image))
        else:
            image = load_image_from_url(url)
            if image is not None:
                images[key] = ptk.PhotoImage(image)
    return images

images = load_images()

# Verify if images were loaded successfully
if not images or "logo" not in images:
    messagebox.showerror("Error", "There was a problem loading images. Please check the URLs or your internet connection.")
    root.destroy()

# Heading
Heading = LabelFrame(root, bd=2, relief="groove", bg="light yellow")
Heading.place(x=0, y=0, width=1380, height=55)

label_logo = Label(Heading, image=images['logo'])
label_logo.grid(row=0, column=0)

name = Label(Heading, text="BookVerse", font="arial 20 bold italic", bg="orange", fg="blue")
name.grid(row=0, column=1)

tagline = Label(Heading, text="A vibrant hub for Bibliophile", font="magneto 16 italic", fg="blue", bg="orange")
tagline.grid(row=0, column=2, padx=280)

# Products
Products_frame = LabelFrame(root, bd=2, relief="groove", text="Products", font="arial 16 bold", fg="dark blue")
Products_frame.place(x=310, y=60, width=1040, height=620)

# Button Frame
Button_frame = LabelFrame(root, bd=2, relief="groove")
Button_frame.place(x=2, y=60, width=300, height=380)

# Variable Lists for Cart
m_list = []  # Horror products
fa_list = [] # Kids products
my_list = [] # Mystery products
hu_list = [] # Humour products

# Function to Hide Frames
def HideAllFrames():
    for widget in Products_frame.winfo_children():
        widget.destroy()

# User Dashboard Function
def show_user_dashboard():
    HideAllFrames()
    dashboard_label = Label(Products_frame, text="User Dashboard", font="times 20 bold", fg="blue")
    dashboard_label.grid(row=0, column=0, padx=20)

    # User details entry
    Label(Products_frame, text="Name:").grid(row=1, column=0, sticky="e")
    name_entry = Entry(Products_frame, width=30)
    name_entry.grid(row=1, column=1, pady=5)

    Label(Products_frame, text="Age:").grid(row=2, column=0, sticky="e")
    age_entry = Entry(Products_frame, width=30)
    age_entry.grid(row=2, column=1, pady=5)

    Label(Products_frame, text="Gender:").grid(row=3, column=0, sticky="e")
    gender_var = StringVar()
    gender_var.set("Select")
    gender_option_menu = OptionMenu(Products_frame, gender_var, "Male", "Female", "Other")
    gender_option_menu.grid(row=3, column=1, pady=5)
    
    Label(Products_frame, text="Favorite Book Genre:").grid(row=4, column=0, sticky="e")
    genre_entry = Entry(Products_frame, width=30)
    genre_entry.grid(row=4, column=1, pady=5)

    # Save Button
    def save_user_info():
        name = name_entry.get()
        age = age_entry.get()
        gender = gender_var.get()
        favorite_genre = genre_entry.get()
        
        if not name or not age or gender == "Select" or not favorite_genre:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Displaying the user information in an info box for simplicity
        messagebox.showinfo("User Info", f"Name: {name}\nAge: {age}\nGender: {gender}\nFavorite Genre: {favorite_genre}")

    save_button = Button(Products_frame, text="Save Info", command=save_user_info)
    save_button.grid(row=5, columnspan=2, pady=20)

# Button Callback for User Dashboard
user_dashboard_button = Button(Heading, text="User Dashboard", font="times 17 bold", bg="black", fg="white", activebackground="purple", command=show_user_dashboard)
user_dashboard_button.grid(row=0, column=3)

# Example Product Functions
def mCall():
    HideAllFrames()
    m_Label = Label(Products_frame, text="Horror", font="times 15 bold", fg="gold", bg="black")
    m_Label.grid(row=0, column=0, padx=20)

    for i in range(3):
        lf = LabelFrame(Products_frame, bd=2, relief="groove")
        lf.place(x=5 + i * 205, y=35, width=180, height=280)
        Label(lf, image=images['horror'][i]).grid(row=0, column=0)
        Label(lf, text=f"Book{i+1}", font="arial 9").grid(row=1, column=0)
        
        var = StringVar()
        var.set("Read")  # default option
        options = ["Read", "Purchase", "Reviews", "Discussion"]
        OptionMenu(lf, var, *options).place(x=30, y=212)
        
        Button(lf, text="Select", command=lambda name=f"Book{i+1}", var=var: AddHorrorToCart(name, var.get())).place(x=50, y=245)

# Select Function for Horror
def AddHorrorToCart(name, option):
    global m_list
    price = mPrice(option)
    if messagebox.askyesno("Purchase Confirmation", f"Are you sure that you want to add {name} to the cart?"):
        m_list.append([name, price, option])
        messagebox.showinfo("Product Status", f"{name} ({option}) is successfully added to the cart.")

# Price mapping for options
def mPrice(option):
    if "Read" in option:
        return 100
    elif "Purchase" in option:
        return 180
    elif "Reviews" in option:
        return 270
    elif "Discussion" in option:
        return 360
    return 0

# Functions for Displaying Kids Products
def faCall():
    HideAllFrames()
    fa_Label = Label(Products_frame, text="Kids", font="times 15 bold", fg="gold", bg="black")
    fa_Label.grid(row=0, column=0, padx=10)

    for i in range(3):
        lf = LabelFrame(Products_frame, bd=2, relief="groove")
        lf.place(x=5 + i * 205, y=35, width=180, height=280)
        Label(lf, image=images['kids'][i]).grid(row=0, column=0)
        Label(lf, text=f"Book{i+1}", font="arial 9", justify="center").grid(row=1, column=0)
        
        var = StringVar()
        var.set("Read")  # default option
        options = ["Read", "Purchase", "Reviews", "Discussion"]
        OptionMenu(lf, var, *options).place(x=30, y=212)
        
        Button(lf, text="Select", command=lambda name=f"Book{i+1}", var=var: AddKidsToCart(name, var.get())).place(x=50, y=245)

# Select Function for Kids
def AddKidsToCart(name, option):
    global fa_list
    price = 20 * (1 + (fa_list.count(name) % 3))  # Dynamic pricing based on the option selected
    if messagebox.askyesno("Purchase Confirmation", f"Are you sure that you want to add {name} to the cart?"):
        fa_list.append([name, price, option])
        messagebox.showinfo("Product Status", f"{name} ({option}) is successfully added to the cart.")

# Functions for Displaying Mystery Products
def myCall():
    HideAllFrames()
    my_Label = Label(Products_frame, text="Mystery", font="times 15 bold", fg="gold", bg="black")
    my_Label.grid(row=0, column=0, padx=10)

    for i in range(3):
        lf = LabelFrame(Products_frame, bd=2, relief="groove")
        lf.place(x=5 + i * 205, y=35, width=180, height=280)
        Label(lf, image=images['mystery'][i]).grid(row=0, column=0)
        Label(lf, text=f"Mystery Book {i + 1}", font="arial 9").grid(row=1, column=0)
        
        var = StringVar()
        var.set("Read")  # default option
        options = ["Read", "Purchase", "Reviews", "Discussion"]
        OptionMenu(lf, var, *options).place(x=30, y=212)
        
        Button(lf, text="Select", command=lambda name=f"Mystery Book {i+1}", var=var: AddMysteryToCart(name, var.get())).place(x=50, y=245)

# Select Function for Mystery
def AddMysteryToCart(name, option):
    global my_list
    price = mPrice(option)
    if messagebox.askyesno("Purchase Confirmation", f"Are you sure that you want to add {name} to the cart?"):
        my_list.append([name, price, option])
        messagebox.showinfo("Product Status", f"{name} ({option}) is successfully added to the cart.")

# Functions for Displaying Humour Products
def huCall():
    HideAllFrames()
    hu_Label = Label(Products_frame, text="Humour", font="times 15 bold", fg="gold", bg="black")
    hu_Label.grid(row=0, column=0, padx=10)

    for i in range(3):
        lf = LabelFrame(Products_frame, bd=2, relief="groove")
        lf.place(x=5 + i * 205, y=35, width=180, height=280)
        Label(lf, image=images['humour'][i]).grid(row=0, column=0)
        Label(lf, text=f"Humour Book {i + 1}", font="arial 9").grid(row=1, column=0)
        
        var = StringVar()
        var.set("Read")  # default option
        options = ["Read", "Purchase", "Reviews", "Discussion"]
        OptionMenu(lf, var, *options).place(x=30, y=212)
        
        Button(lf, text="Select", command=lambda name=f"Humour Book {i+1}", var=var: AddHumourToCart(name, var.get())).place(x=50, y=245)

# Select Function for Humour
def AddHumourToCart(name, option):
    global hu_list
    price = mPrice(option)
    if messagebox.askyesno("Purchase Confirmation", f"Are you sure that you want to add {name} to the cart?"):
        hu_list.append([name, price, option])
        messagebox.showinfo("Product Status", f"{name} ({option}) is successfully added to the cart.")


# Product Buttons
m_button = Button(Button_frame, text="Horror", font="times 20 bold", width=17, bd=6, bg="black", fg="white", activebackground="light blue", command=mCall)
m_button.grid(row=0, column=0, padx=5, pady=5)

fa_button = Button(Button_frame, text="Kids", font="times 20 bold", width=17, bd=6, bg="black", fg="white", activebackground="light blue", command=faCall)
fa_button.grid(row=1, column=0, padx=5, pady=5)

my_button = Button(Button_frame, text="Mystery", font="times 20 bold", width=17, bd=6, bg="black", fg="white", activebackground="light blue", command=myCall)
my_button.grid(row=2, column=0, padx=5, pady=5)

hu_button = Button(Button_frame, text="Humour", font="times 20 bold", width=17, bd=6, bg="black", fg="white", activebackground="light blue", command=huCall)
hu_button.grid(row=3, column=0, padx=5, pady=5)

# Start the Tkinter main loop
root.mainloop()