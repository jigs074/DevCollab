from flask import Flask, render_template, request, redirect, url_for, session, jsonify,Blueprint

import json, hashlib, getpass, os , sys
from cryptography.fernet import Fernet
from datetime import datetime 

app = Flask(__name__)
app.secret_key = os.urandom(24)

from BlogPosts import blog_bp
from Authentication import auth_bp 
# Register the blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(blog_bp, url_prefix='/blog', name='blog_blueprint') 

# Function for hashing the password 

users = []
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_status', methods=['OPTIONS'])
def options_route():
    routes_info = {}
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        route_path = rule.rule.lstrip("/")
        routes_info[route_path] = methods

    response_text = "\n".join([f"{route}: {methods}" for route, methods in routes_info.items()])
    formatted_response = f"""
Options Request Successful
Available Routes:
{response_text}
"""

    response = jsonify({'message': formatted_response})
    allowed_methods = [rule.methods for rule in app.url_map.iter_rules()]
    allowed_methods = [method for methods in allowed_methods for method in methods]
    response.headers.add('Allow', ', '.join(allowed_methods))
    return response


if __name__ == "__main__":
    app.run(debug = True)