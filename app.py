from flask import Flask, render_template, request, redirect, url_for, session, jsonify,Blueprint

import json, hashlib, getpass, os , pyperclip, sys
from cryptography.fernet import Fernet
from datetime import datetime 

app = Flask(__name__)
app.secret_key = os.urandom(24)

from BlogPosts import blog_bp
from Authentication import auth_bp 
# Register the blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)

# Function for hashing the password 

users = []
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True)
    
    



    