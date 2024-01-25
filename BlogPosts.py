
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint

import json, hashlib, getpass, os , pyperclip, sys
from cryptography.fernet import Fernet
from datetime import datetime 

blog_bp = Blueprint('blog',__name__)


@blog_bp.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('blogpost.html', username=session['username'])
        else:
            return jsonify({'error': 'User not logged in'}), 401
    elif request.method == 'POST':
        if 'username' in session:
            
            user_blog_file = f"{session['username']}_blog.json"
           
            blog_content = request.json.get('blog_content')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_post = {'timestamp': timestamp,'content':blog_content}
            if os.path.exists(user_blog_file):
                with open(user_blog_file, 'r') as file:
                    user_blog_data = json.load(file)
            else:
                user_blog_data = []
                
            user_blog_data.append(new_post)
            
            with open(user_blog_file, "w") as file:
                json.dump(user_blog_data, file, indent =4)
                
            return jsonify({'message': 'Blog post submitted successfully'})
        else:
            return jsonify({'error': 'User not logged in'}), 401

    

@blog_bp.route('/all_blog_posts', methods=['GET'])
def all_blog_posts():
    if 'username' in session:
        user_blog_file = f"{session['username']}_blog.json"

        if os.path.exists(user_blog_file):
            with open(user_blog_file, 'r') as file:
                user_blog_data = json.load(file)
        else:
            user_blog_data = []
        username = session['username']
        response_data = {'username':username, 'blog_data': user_blog_data}
        data =  jsonify(response_data)
        return data 
        
    else:
        return redirect(url_for('home'))
                
@blog_bp.route('/display_blog', methods=['GET'])
def display_blog():
    return render_template('all_blog_posts.html')