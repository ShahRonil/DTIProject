from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import threading

# Flask setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reddit_clone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Database models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(data['password'])
    
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    data = request.get_json()
    title = data['title']
    content = data['content']
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created!"})

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{"title": post.title, "content": post.content} for post in posts])

def run_flask():
    app.run(debug=True, use_reloader=False)  # Disable reloader if running in a thread

# Tkinter GUI
class RedditCloneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reddit Clone")

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=0, column=1)
        self.username_label = tk.Label(self.login_frame, text="Username: ")
        self.username_label.grid(row=0, column=0)

        self.password_entry = tk.Entry(self.login_frame, show='*', width=30)
        self.password_entry.grid(row=1, column=1)
        self.password_label = tk.Label(self.login_frame, text="Password: ")
        self.password_label.grid(row=1, column=0)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=5)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1, pady=5)

        self.post_frame = None

        self.posts_text = scrolledtext.ScrolledText(self.root, width=50, height=15, state='disabled')
        self.posts_text.pack(padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = requests.post('http://127.0.0.1:5000/login', json={"username": username, "password": password})
        if response.status_code == 200:
            messagebox.showinfo("Success", "Login successful!")
            self.show_post_frame()
            self.refresh_posts()  # Refresh posts on login
        else:
            messagebox.showerror("Error", response.json()['message'])

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = requests.post('http://127.0.0.1:5000/register', json={"username": username, "password": password})
        messagebox.showinfo("Info", response.json()['message'])

    def show_post_frame(self):
        if self.post_frame:
            self.post_frame.destroy()

        self.post_frame = tk.Frame(self.root)
        self.post_frame.pack(padx=10, pady=10)

        self.title_entry = tk.Entry(self.post_frame, width=30)
        self.title_entry.grid(row=0, column=1)
        self.title_label = tk.Label(self.post_frame, text="Post Title: ")
        self.title_label.grid(row=0, column=0)

        self.content_entry = tk.Text(self.post_frame, width=30, height=5)
        self.content_entry.grid(row=1, column=1)
        self.content_label = tk.Label(self.post_frame, text="Content: ")
        self.content_label.grid(row=1, column=0)

        self.submit_button = tk.Button(self.post_frame, text="Submit Post", command=self.submit_post)
        self.submit_button.grid(row=2, column=0, pady=5)

        self.view_posts_button = tk.Button(self.post_frame, text="Refresh Posts", command=self.refresh_posts)
        self.view_posts_button.grid(row=2, column=1, pady=5)

    def submit_post(self):
        title = self.title_entry.get()
        content = self.content_entry.get("1.0", tk.END).strip()  # Get the content from the text widget

        response = requests.post('http://127.0.0.1:5000/submit', json={"title": title, "content": content})
        messagebox.showinfo("Info", response.json()['message'])
        self.title_entry.delete(0, tk.END)  # Clear title entry after submitting
        self.content_entry.delete("1.0", tk.END)  # Clear content area after submitting
        self.refresh_posts()  # Refresh posts after submitting

    def refresh_posts(self):
        response = requests.get('http://127.0.0.1:5000/posts')
        if response.status_code == 200:
            posts = response.json()
            self.posts_text.config(state='normal')  # Allow editing to update text
            self.posts_text.delete('1.0', tk.END)  # Clear the text before adding new posts
            for post in posts:
                self.posts_text.insert(tk.END, f"{post['title']}\n{post['content']}\n\n")  # Add title and content
            self.posts_text.config(state='disabled')  # Disable editing again

if __name__ == '__main__':
    # Run Flask in a separate thread
    thread = threading.Thread(target=run_flask)
    thread.start()

    # Run the Tkinter GUI
    root = tk.Tk()
    app = RedditCloneApp(root)
    root.mainloop()