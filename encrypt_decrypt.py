import cv2
import os
import tkinter as tk
from tkinter import ttk, filedialog

img = None  # Initialize img as a global variable
key = ""
msg = ""
c = {}  # Define c as a global variable
original_file_path = ""
encrypted_file_path = ""

def encrypt():
    global img, key, msg, original_file_path, encrypted_file_path
    msg = entry_msg.get()
    key = entry_key.get()

    d = {}

    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)

    m = 0
    n = 0
    z = 0

    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    # Save encrypted image with filename format: chosen_file_name_encrypt.jpg
    encrypted_file_name = os.path.basename(original_file_path).split(".")[0] + "_encrypt.jpg"
    encrypted_file_path = os.path.join(os.path.expanduser("~"), encrypted_file_name)
    cv2.imwrite(encrypted_file_path, img)

    label_result_encrypt.config(text="Message has been successfully encrypted!\nEncrypted file saved to:\n" + encrypted_file_path)

def decrypt():
    global img, key, msg, c
    message = ""
    n = 0
    m = 0
    z = 0

    key1 = entry_decrypt_key.get()

    if key == key1:
        for i in range(len(msg)):
            message = message + c[int(img[n, m, z])]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3
        label_result_decrypt.config(text="Decrypted message is: " + message)
    else:
        label_result_decrypt.config(text="Sorry!! The secret key entered by you is incorrect...")

def open_file():
    global img, original_file_path, encrypted_file_path
    file_path = filedialog.askopenfilename()
    img = cv2.imread(file_path).copy()
    original_file_path = file_path
    encrypted_file_path = ""
    label_selected_file.config(text="Selected File: " + os.path.basename(file_path))

# Create GUI
root = tk.Tk()
root.title("Image Encryption/Decryption")

# Set background color for the entire screen
bg_color = "lightgreen"
root.configure(bg=bg_color)

# Set a fixed window size
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center position for the root window
x_position = int((screen_width - window_width) / 2)
y_position = int((screen_height - window_height) / 2)

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Encryption Tab
frame_encrypt = tk.Frame(notebook, bg=bg_color)
notebook.add(frame_encrypt, text="Encryption")

label_insert_image = tk.Label(frame_encrypt, text="Insert Image:", fg="black", bg=bg_color, font=("Helvetica", 10))
label_insert_image.grid(row=0, column=0, sticky="e", pady=5)

btn_open = tk.Button(frame_encrypt, text="Open Image", command=open_file, font=("Helvetica", 10))
btn_open.grid(row=0, column=1, sticky="w", pady=5)

label_selected_file = tk.Label(frame_encrypt, text="Selected File: ", bg=bg_color, font=("Helvetica", 10))
label_selected_file.grid(row=1, column=0, columnspan=2, pady=5)

label_msg = tk.Label(frame_encrypt, text="Enter secret message:", bg=bg_color, font=("Helvetica", 10))
label_msg.grid(row=2, column=0, sticky="e", pady=5)

entry_msg = tk.Entry(frame_encrypt, font=("Helvetica", 10))
entry_msg.grid(row=2, column=1, sticky="w", pady=5)

label_key = tk.Label(frame_encrypt, text="Enter key:", bg=bg_color, font=("Helvetica", 10))
label_key.grid(row=3, column=0, sticky="e", pady=5)

entry_key = tk.Entry(frame_encrypt, font=("Helvetica", 10))
entry_key.grid(row=3, column=1, sticky="w", pady=5)

btn_encrypt = tk.Button(frame_encrypt, text="Encrypt", command=encrypt, bg="green", fg="white", font=("Helvetica", 10))
btn_encrypt.grid(row=4, column=0, columnspan=2, pady=10)

label_result_encrypt = tk.Label(frame_encrypt, text="", bg=bg_color, font=("Helvetica", 14))
label_result_encrypt.grid(row=5, column=0, columnspan=2, pady=5)

# Decryption Tab
frame_decrypt = tk.Frame(notebook, bg=bg_color)
notebook.add(frame_decrypt, text="Decryption")

label_decrypt_key = tk.Label(frame_decrypt, text="Enter secret key:", bg=bg_color, font=("Helvetica", 10))
label_decrypt_key.grid(row=0, column=0, sticky="e", pady=5)

entry_decrypt_key = tk.Entry(frame_decrypt, font=("Helvetica", 10))
entry_decrypt_key.grid(row=0, column=1, sticky="w", pady=5)

btn_decrypt = tk.Button(frame_decrypt, text="Decrypt", command=decrypt, bg="blue", fg="white", font=("Helvetica", 10))
btn_decrypt.grid(row=1, column=0, columnspan=2, pady=10)

label_result_decrypt = tk.Label(frame_decrypt, text="", bg=bg_color, font=("Helvetica", 10))
label_result_decrypt.grid(row=2, column=0, columnspan=2, pady=5)

root.mainloop()
