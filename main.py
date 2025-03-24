from tkinter import *
from tkinter import messagebox, font
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Function to download and return an image from a URL
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        return img
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")
        messagebox.showerror("Error", "Failed to load image from URL.")
        return None
    except IOError:
        print("Error opening image.")
        messagebox.showerror("Error", "Failed to open the image file.")
        return None

# Main application class
class UserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Login/Sign Up")
        
        # Set the window to full screen
        self.root.attributes('-fullscreen', True)
        
        # Initialize selected_user_type variable
        self.selected_user_type = StringVar()

        # Load background image from URL
        self.image_url = "https://tse2.mm.bing.net/th?id=OIP.-DBUP7TUeRZwFkyc63yNJgHaFj&pid=Api&P=0&h=180"
        self.bg_image = load_image_from_url(self.image_url)

        # Create a label for background
        self.bg_label = Label(self.root)
        self.bg_label.place(relwidth=1, relheight=1)  # Fill the entire window
        self.update_background_image()

        # Bind the escape key to exit full screen
        self.root.bind("<Escape>", self.toggle_fullscreen)
        # Bind window resize
        self.root.bind('<Configure>', self.update_background_image)

        # Create the initial GUI elements
        self.create_initial_gui()

    def update_background_image(self, event=None):
        if self.bg_image is not None:
            # Resize the image to fit the window
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            resized_image = self.bg_image.resize((width, height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            self.bg_label.config(image=self.bg_photo)

    def toggle_fullscreen(self, event=None):
        current_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_fullscreen)

    def create_initial_gui(self):
        title_font = font.Font(family="Times New Roman", size=36, weight="bold")  # Larger font size
        Label(self.root, text="Welcome to Book Haven", font=title_font, bg="#f8f1e7", fg="#6a4f4b").pack(pady=(40, 20))

        button_font = font.Font(family="Times New Roman", size=18)  # Larger font size for buttons

        Button(self.root, text="Author", command=lambda: self.show_login_signup("Author"), 
               bg="#d4b09c", fg="white", font=button_font, width=20, height=2).pack(pady=10)
        
        Button(self.root, text="Reader", command=lambda: self.show_login_signup("Reader"), 
               bg="#d4b09c", fg="white", font=button_font, width=20, height=2).pack(pady=10)

    def show_login_signup(self, user_type):
        self.selected_user_type.set(user_type)
        self.clear_window()
        self.bg_label = Label(self.root)
        self.bg_label.place(relwidth=1, relheight=1)  # Fill the entire window
        self.update_background_image()

        title_font = font.Font(family="Times New Roman", size=30, weight="bold")  # Larger font size
        Label(self.root, text=f"{user_type} Login/Sign Up", font=title_font, bg="#f8f1e7", fg="#6a4f4b").pack(pady=(40, 20))

        frame = Frame(self.root, bg="#f8f1e7")
        frame.pack(pady=20)

        # Modify input fields
        entry_font = font.Font(family="Times New Roman", size=18)  # Larger font size for entries

        # Set grid layout with centering and proper padding
        Label(frame, text="Username:", bg="#f8f1e7", font=entry_font).grid(row=0, column=0, pady=10, padx=(0, 10), sticky=E)
        self.username_entry = Entry(frame, font=entry_font, width=30)
        self.username_entry.grid(row=0, column=1, pady=10)

        Label(frame, text="Password:", bg="#f8f1e7", font=entry_font).grid(row=1, column=0, pady=10, padx=(0, 10), sticky=E)
        self.password_entry = Entry(frame, show='*', font=entry_font, width=30)
        self.password_entry.grid(row=1, column=1, pady=10)

        # Buttons with proportional layout
        button_width = 15
        Button(frame, text="Login", command=self.login, bg="#6a4f4b", fg="white", width=button_width, 
               activebackground="#5a3c3e", font=entry_font, height=2).grid(row=2, column=0, pady=15, padx=(0, 10), sticky=E)
        
        Button(frame, text="Sign Up", command=self.signup, bg="#6a4f4b", fg="white", width=button_width,
               activebackground="#5a3c3e", font=entry_font, height=2).grid(row=2, column=1, pady=15)

        Button(self.root, text="Back", command=self.back_to_main, fg='blue', bg="#d4b09c", font=entry_font, height=2).pack(pady=(10, 40))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.selected_user_type.get()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        if user_type == "Author" and username == "abcd" and password == "1234":
            messagebox.showinfo("Login Success", f"Welcome Tech Support {username}. You are logged in as Tech Support.")
        else:
            messagebox.showinfo("Login Success", f"Welcome {username}, you logged in as a {user_type}.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.selected_user_type.get()

        if not username or not password:
            messagebox.showerror("Sign Up Error", "Please enter both username and password.")
            return

        messagebox.showinfo("Sign Up Success", f"{user_type} account created for {username}.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def back_to_main(self):
        self.clear_window()
        self.create_initial_gui()

if __name__ == "__main__":
    root = Tk()
    app = UserApp(root)
    root.mainloop()