from flask import Flask, render_template, request, redirect, url_for, session

import json, hashlib, getpass, os , pyperclip, sys
from cryptography.fernet import Fernet
from datetime import datetime 

app = Flask(__name__)
app.secret_key = os.urandom(24)
# Function for hashing the password 
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode())
    return sha256.hexdigest()


# Function for generating the secret key 

def generate_key():
    return Fernet.generate_key()

def initialize_cipher(key):
    return Fernet(key)

# Function to encrypt a password

def encrypt_password(cipher, password):
    return cipher.encrypt(password.encode()).decode()

# Function to decrypt a password 

def decrypt_password(cipher, encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register',methods=['GET', 'POST'])
# Function to register you.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        hashed_password = hash_password(password)
        user_data = {'username': username, 'password': hashed_password}
        file_name = 'user_data.json'

        try:
            with open(file_name, 'r') as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = []
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            existing_data = []

        existing_data.append(user_data)

        with open(file_name, 'w') as file:
            json.dump(existing_data, file, indent=4)
            print("\n[+] Registration complete!!\n")

       

    return render_template('index.html')

# Function to log you in.
@app.route('/login', methods=['POST'])
def login():
    try:
      
        username = request.form.get('login_username')
        print(username)
        entered_password = request.form.get('login_password')
        entered_password_hash = hash_password(entered_password)
        with open('user_data.json', 'r') as file:
            user_data_list = json.load(file)
            
        for user_data in user_data_list:
            if user_data.get('username') == username and user_data.get('password') == entered_password_hash:
                session['username'] = username 
                print("Login Successfull..")
                return redirect(url_for('blog'))
                
        else:
            print("Invalid Login Credentials")
            sys.exit()
            
        

        #print(user_data_list)

        # Iterate over each user dictionary in the list
    
# If no matching user is found


    except FileNotFoundError:
        print("\n[-] You have not registered. Please do that.\n")

    return render_template('index.html')  # This is outside the try-except block

@app.route('/blog', methods = ['GET' , 'POST'])

def blog():
    if 'username' in session:
        user_blog_file = f"{session['username']}_blog.json"
        
        if request.method == 'POST':
            # Handle the blog post submissions here 
            blog_content = request.form.get('blog_content')
            timestamp = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
            new_post = {'timestamp': timestamp, 'content': blog_content}
            
            if os.path.exists(user_blog_file):
                with open(user_blog_file, 'r') as file:
                    user_blog_data = json.load(file)
            else:
                user_blog_data = []
                
            user_blog_data.append(new_post)
            with open(user_blog_file, "w") as file:
                json.dump(user_blog_data, file, indent =4)
            
            
            print(f"User '{session['username']}' submitted a blog post: {blog_content}")
            
            
        return render_template('blogpost.html', username = session['username'])
    
    else:
        return redirect(url_for('home'))
    

@app.route('/all_blog_posts', methods=['GET'])
def all_blog_posts():
    if 'username' in session:
        user_blog_file = f"{session['username']}_blog.json"

        if os.path.exists(user_blog_file):
            with open(user_blog_file, 'r') as file:
                user_blog_data = json.load(file)
        else:
            user_blog_data = []

        return render_template('all_blog_posts.html', username=session['username'], blog_data=user_blog_data)
    else:
        return redirect(url_for('home'))
    
    
    
    
    
            

if __name__ == "__main__":
    app.run(debug = True)
    
    



    