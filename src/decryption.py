import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import padding

import tkinter as tk

from tkinter import messagebox



# Function to decrypt a file

def decrypt_file(file_path, key):

    backend = default_backend()



    # Read encrypted data from file

    with open(file_path, 'rb') as f:

        encrypted_data = f.read()



    # Extract IV (first 16 bytes)

    iv = encrypted_data[:16]

    encrypted_file_data = encrypted_data[16:]



    # Create a cipher object for AES decryption

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    decryptor = cipher.decryptor()



    # Decrypt the data

    decrypted_padded_data = decryptor.update(encrypted_file_data) + decryptor.finalize()



    # Unpad the decrypted data

    unpadder = padding.PKCS7(128).unpadder()

    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()



    # Write the decrypted data back to the file

    with open(file_path, 'wb') as f:

        f.write(decrypted_data)



# Function to decrypt files in a specific folder

def decrypt_folder(folder_path, key):

    # Decrypt files in the specified folder

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            try:

                file_path = os.path.join(root, file)

                decrypt_file(file_path, key)

                print(f"Decrypted: {file_path}")

            except Exception as e:

                print(f"Failed to decrypt {file_path}: {e}")



    # Show a pop-up that decryption is complete

    show_decryption_complete_note()



# Function to display decryption complete pop-up

def show_decryption_complete_note():

    root = tk.Tk()

    root.withdraw()  # Hide the root window

    messagebox.showinfo("Decryption Complete", "Your files have been decrypted.")

    root.mainloop()



# The 256-bit AES key for decryption (replace this with the actual key)

key = bytes.fromhex('hexadecimal_key')



# Define the folder you want to decrypt

target_folder = "/home/"  # Replace with the actual folder path



# Start decryption on the specified folder

decrypt_folder(target_folder, key)
