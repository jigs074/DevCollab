from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint

import json, hashlib, getpass, os , sys
from cryptography.fernet import Fernet
from datetime import datetime 

from Database import export_to_mongodb, import_from_mongodb

auth_bp = Blueprint('auth',__name__)

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


@auth_bp.route('/register',methods=['GET', 'POST'])
# Function to register you.
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        hashed_password = hash_password(password)
        user_data = {'username': username, 'password': hashed_password}
        file_name = 'user_data.json'
        export_to_mongodb("User_Database", user_data)
        try:
            with open(file_name, 'r') as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = []
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            existing_data = []

        user_data['_id'] = None
        existing_data.append(user_data)

        with open(file_name, 'w') as file:
            json.dump(existing_data, file, indent=4)
            print("\n[+] Registration complete!!\n")

       

    return render_template('index.html')

# Function to log you in.
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
      
        username = request.form.get('login_username')
        print(username)
        entered_password = request.form.get('login_password')
        entered_password_hash = hash_password(entered_password)
        #user_data_list = import_from_mongodb("User_Database")
        with open('user_data.json', 'r') as file:
            user_data_list = json.load(file)
            
        for user_data in user_data_list:
            if user_data.get('username') == username and user_data.get('password') == entered_password_hash:
                session['username'] = username 
                print("Login Successfull..")
                return redirect(url_for('blog.blog'))
                
        else:
            print("Invalid Login Credentials")
            sys.exit()
            
        

        #print(user_data_list)

        # Iterate over each user dictionary in the list
    
# If no matching user is found


    except FileNotFoundError:
        print("\n[-] You have not registered. Please do that.\n")

    return render_template('index.html')  # This is outside the try-except block
