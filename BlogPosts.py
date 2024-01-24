from flask import Flask, render_template, request, redirect, url_for, session, jsonify 

import json, hashlib, getpass, os , pyperclip, sys
from cryptography.fernet import Fernet
from datetime import datetime 


app = Flask(__name__)

# @app.route('/blog', methods=['POST'])
# def post_blog():
#     if 'username' in session:
#         user_blog_file = f"{session['username']}_blog.json"

#         blog_content = request.form.get('blog_content')
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         new_post = {'timestamp': timestamp, 'content': blog_content}

#         if os.path.exists(user_blog_file):
#             with open(user_blog_file, 'r') as file:
#                 user_blog_data = json.load(file)
#         else:
#             user_blog_data = []

#         user_blog_data.append(new_post)

#         with open(user_blog_file, "w") as file:
#             json.dump(user_blog_data, file, indent=4)

#         print(f"User '{session['username']}' submitted a blog post: {blog_content}")

#         return jsonify({'message': 'Blog post submitted successfully'})
#     else:
#         return jsonify({'error': 'User not logged in'}), 401
    
    
    
# @app.route('/blog', methods=['GET'])
# def get_blog():
#    return render_template('blogpost.html', username = session['username'])

# @app.route('/all_blog_posts', methods=['GET'])
# def all_blog_posts():
#     if 'username' in session:
#         user_blog_file = f"{session['username']}_blog.json"

#         if os.path.exists(user_blog_file):
#             with open(user_blog_file, 'r') as file:
#                 user_blog_data = json.load(file)
#         else:
#             user_blog_data = []

#         return render_template('all_blog_posts.html', username=session['username'], blog_data=user_blog_data)
#     else:
#         return redirect(url_for('home'))
    
