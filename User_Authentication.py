from flask import Flask, render_template, request, redirect, url_for, session

import json, hashlib, getpass, os , pyperclip, sys
from cryptography.fernet import Fernet

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



    