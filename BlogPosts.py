from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint

import json, hashlib, getpass, os , sys
from cryptography.fernet import Fernet
from datetime import datetime 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Database import *

blog_bp = Blueprint('blog',__name__)

uri = "mongodb://localhost:27017"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["Blogpost_Database"]

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
            
            #blogpost database
            username = session['username']
            collection = db[username]

            new_post['_id'] = None ## fix '_id' field
            collection.insert_one(new_post) ##insert new post into database collection
            user_blog_data.append(new_post)
            
            with open(user_blog_file, "w") as file:
                json.dump(user_blog_data, file, indent =4)
                
            return jsonify({'message': 'Blog post submitted successfully'})
        else:
            return jsonify({'error': 'User not logged in'}), 401
    

@blog_bp.route('/edit_blog_post/<int:post_index>', methods=['PATCH'])
def patch_blog_post(post_index):
    if 'username' in session:
        user_blog_file = f"{session['username']}_blog.json"

        if os.path.exists(user_blog_file):
            with open(user_blog_file, 'r') as file:
                user_blog_data = json.load(file)

            if post_index < len(user_blog_data):
                # Assuming the request data contains the updated content
                update_data = request.get_json()

                # Update the entire content with the new content
                user_blog_data[post_index]['content'] = update_data.get('content', '')

                # Save the updated data back to the file
                with open(user_blog_file, 'w') as file:
                    json.dump(user_blog_data, file)

                # Now, update the MongoDB record
                username = session['username']
                edit_field(username, user_blog_data[post_index])

                return jsonify({'message': 'Blog post updated successfully'})
            else:
                return jsonify({'error': 'Invalid blog post index'})
        else:
            return jsonify({'error': 'User blog file not found'})
    else:
        return jsonify({'error': 'User not logged in'})

    
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


@blog_bp.route('/edit_blog_post/<int:post_index>', methods=['PUT'])
def edit_blog_post(post_index):
    if 'username' in session:
        user_blog_file = f"{session['username']}_blog.json"

        if os.path.exists(user_blog_file):
            with open(user_blog_file, 'r') as file:
                user_blog_data = json.load(file)

            if post_index < len(user_blog_data):
                # Assuming the request data contains the updated blog post content
                updated_content = request.get_json()
                
                # Update the blog post with the new content
                user_blog_data[post_index]['content'] = updated_content.get('content', '')

                # Save the updated data back to the file
                with open(user_blog_file, 'w') as file:
                    json.dump(user_blog_data, file)

                return jsonify({'message': 'Blog post updated successfully'})
            else:
                return jsonify({'error': 'Invalid blog post index'})
        else:
            return jsonify({'error': 'User blog file not found'})
    else:
        return jsonify({'error': 'User not logged in'})



@blog_bp.route('/delete_blog_post/<int:post_index>', methods=['DELETE'])
def delete_blog_post(post_index):
    if 'username' in session:
        user_blog_file = f"{session['username']}_blog.json"

        if os.path.exists(user_blog_file):
            with open(user_blog_file, 'r') as file:
                user_blog_data = json.load(file)

            if post_index < len(user_blog_data):
                # Remove the specified blog post
                deleted_post = user_blog_data.pop(post_index)

                # Save the updated data back to the file
                with open(user_blog_file, 'w') as file:
                    json.dump(user_blog_data, file)

                # Now, delete the MongoDB record
                username = session['username']
                delete_field(username, deleted_post)

                return jsonify({'message': 'Blog post deleted successfully'})
            else:
                return jsonify({'error': 'Invalid blog post index'})
        else:
            return jsonify({'error': 'User blog file not found'})
    else:
        return jsonify({'error': 'User not logged in'})
