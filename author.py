from tkinter import *
from tkinter import messagebox, filedialog
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Start root application window
root = Tk()
root.title("www.BookVerse - Author Portal")
root.geometry("1360x1000")

# Function to load images from a given URL
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        return Image.open(img_data)
    except requests.RequestException as e:
        print(f"Error fetching image from {url}: {e}")
        return None

# Load images from URLs
def load_images():
    urls = {
        "logo": "https://catalogue.alankarpublication.com/assets/images/gif/1481.gif",  # Logo URL
    }
    images = {}
    for key, url in urls.items():
        images[key] = load_image_from_url(url)
        if images[key] is not None:
            images[key] = ImageTk.PhotoImage(images[key])
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

name = Label(Heading, text="BookVerse Author Portal", font="arial 20 bold italic", bg="orange", fg="blue")
name.grid(row=0, column=1)

tagline = Label(Heading, text="Connect, Share, and Manage Your Works", font="magneto 16 italic", fg="blue", bg="orange")
tagline.grid(row=0, column=2, padx=280)

# Global list to store uploaded book data
uploaded_books = []

# Function to clear current frame
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Function to show author dashboard
def show_author_dashboard():
    clear_frame()  # Clear previous widgets
    dashboard_frame = LabelFrame(root, bd=2, relief="groove", text="Upload a Book", font="arial 16 bold", fg="dark blue")
    dashboard_frame.place(x=310, y=60, width=1040, height=620)

    # Book Title input
    Label(dashboard_frame, text="Book Title:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
    title_entry = Entry(dashboard_frame, width=30)
    title_entry.grid(row=0, column=1, pady=10)

    # Amazon Link input
    Label(dashboard_frame, text="Amazon Link:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
    amazon_link_entry = Entry(dashboard_frame, width=30)
    amazon_link_entry.grid(row=1, column=1, pady=10)

    # Book Cover Upload
    Label(dashboard_frame, text="Upload Book Cover:").grid(row=2, column=0, padx=10, pady=10, sticky=W)

    def upload_cover():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            messagebox.showinfo("Success", f"Book cover image uploaded: {file_path}")

    upload_button = Button(dashboard_frame, text="Upload", command=upload_cover)
    upload_button.grid(row=2, column=1, pady=10)

    # Submit button
    Button(dashboard_frame, text="Submit", command=lambda: submit_book(title_entry.get(), amazon_link_entry.get())).grid(row=3, columnspan=2, pady=20)

    # Back button to return to main page
    Button(dashboard_frame, text="Back", command=show_main_page).grid(row=4, columnspan=2, pady=10)

# Function to submit book data
def submit_book(title, amazon_link):
    if not title or not amazon_link:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
      
    # Add book data to the list
    uploaded_books.append({"title": title, "amazon_link": amazon_link})
    
    messagebox.showinfo("Success", f"Book '{title}' has been submitted with the Amazon link: {amazon_link}.")

# Function to show uploaded books
def show_uploaded_books():
    clear_frame()  # Clear previous widgets
    books_frame = LabelFrame(root, bd=2, relief="groove", text="Uploaded Books", font="arial 16 bold", fg="dark blue")
    books_frame.place(x=310, y=60, width=1040, height=620)

    if not uploaded_books:
        Label(books_frame, text="No books uploaded yet.", font=("Arial", 12)).pack(pady=20)
        return

    for i, book in enumerate(uploaded_books):
        book_text = f"Title: {book['title']}, Amazon Link: {book['amazon_link']}"
        Label(books_frame, text=book_text, justify="left").pack(anchor="w", padx=10, pady=5)

    # Back button to return to the main page
    Button(books_frame, text="Back", command=show_main_page).pack(pady=20)

# Function to show reviews management
def show_reviews():
    clear_frame()  # Clear previous widgets
    reviews_frame = LabelFrame(root, bd=2, relief="groove", text="Manage Reviews", font="arial 16 bold", fg="dark blue")
    reviews_frame.place(x=310, y=60, width=1040, height=620)

    # Sample reviews data
    reviews = [
        {"user": "Reader1", "review": "Great book!"}, 
        {"user": "Reader2", "review": "Loved the characters."},
        {"user": "Reader3", "review": "Found it boring."}
    ]
    
    Label(reviews_frame, text="Reviews", font="arial 14 bold").grid(row=0, column=0, sticky=W, padx=10, pady=10)

    for i, review in enumerate(reviews):
        review_text = f"{review['user']}: {review['review']}"
        Label(reviews_frame, text=review_text, justify="left").grid(row=i + 1, column=0, sticky=W, padx=10, pady=5)
        
        reply_entry = Entry(reviews_frame, width=30)
        reply_entry.grid(row=i + 1, column=1, padx=10, pady=5)
        
        Button(reviews_frame, text="Reply", command=lambda r=review, reply_entry=reply_entry: reply_to_review(r, reply_entry.get())).grid(row=i + 1, column=2, padx=10, pady=5)

    # Back button to return to the main page
    Button(reviews_frame, text="Back", command=show_main_page).grid(row=len(reviews) + 1, columnspan=3, pady=10)

# Function to reply to a review
def reply_to_review(review, reply):
    if reply:
        messagebox.showinfo("Reply Sent", f"You replied to {review['user']} with: {reply}.")
    else:
        messagebox.showerror("Error", "Reply cannot be empty.")

# Function to show the main page menu
def show_main_page():
    clear_frame()  # Clear previous widgets
    create_custom_menu()  # Create menu buttons
    # Show a message to guide the user
    welcome_label = Label(root, text="Welcome to the Author Portal! Please select an option from the menu.", font=("Arial", 14))
    welcome_label.pack(pady=(200, 10))

# Custom menu creation
def create_custom_menu():
    menu_frame = Frame(root, bd=2, relief="groove", bg="light blue")
    menu_frame.place(x=0, y=55, width=1380, height=50)  # Position below the heading

    # Place a frame to center the buttons
    button_frame = Frame(menu_frame, bg="light blue")
    button_frame.pack(side=TOP, padx=100, pady=5)

    # Dashboard button
    dashboard_button = Button(button_frame, text="Dashboard", font=("Arial", 12), command=show_author_dashboard, width=20)
    dashboard_button.pack(side=LEFT, padx=20)

    # Manage Reviews button
    reviews_button = Button(button_frame, text="Manage Reviews", font=("Arial", 12), command=show_reviews, width=20)
    reviews_button.pack(side=LEFT, padx=20)

    # View Uploaded Books button
    uploaded_books_button = Button(button_frame, text="View Uploaded Books", font=("Arial", 12), command=show_uploaded_books, width=25)
    uploaded_books_button.pack(side=LEFT, padx=20)

# Create the custom menu
create_custom_menu()

# Start the Tkinter main loop with the main page shown
show_main_page()  # Show the main interface at application start
root.mainloop()