import tkinter as tk
from tkinter import ttk

encriptMsg = ''
roter1 = "XULEYABTQWHFSZGOKRCVINMDJP"
roter2 = "BEYCJZXDLGRSUPVMIKWOHFANTQ"
roter3 = "PJGXLNWHIDMBTVFUARKQZYOSCE"
roters = [roter1, roter2, roter3]
roters_used = []

reflector = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'],
             ['O', 'S', 'W', 'Y', 'R', 'Z', 'Q', 'T', 'X', 'P', 'U', 'V', 'N']]

plugboard_pairs = []

def initial_setup():
    global roter1, roter2, roter3
    roter1 = "XULEYABTQWHFSZGOKRCVINMDJP"
    roter2 = "BEYCJZXDLGRSUPVMIKWOHFANTQ"
    roter3 = "PJGXLNWHIDMBTVFUARKQZYOSCE"

def rotate_roters():
    global roter1, roter2, roter3
    rot1 = roter1[:1]
    rot2 = roter1[1:]
    roter1 = rot2 + rot1
    if len(roter1) != len(roter2):
        rot1 = roter2[:1]
        rot2 = roter2[1:]
        roter2 = rot2 + rot1
    if len(roter1) != len(roter3) and len(roter2) != len(roter3):
        rot1 = roter3[:1]
        rot2 = roter3[1:]
        roter3 = rot2 + rot1

def encrypt_message():
    global encriptMsg
    global encrypt_text
    msg = encrypt_text.get("1.0", "end-1c")
    encrypt_msg = ""
    initial_setup()
    for ch in msg:
        if ch.isalpha():
            rotate_roters()
            ch = apply_plugboard(ch)
            en_ch = encrypt_roter(roter1, ch)
            en_ch = encrypt_roter(roter2, en_ch)
            en_ch = encrypt_roter(roter3, en_ch)
            en_ch = reflect(en_ch)
            en_ch = rev_encrypt(roter3, en_ch)
            en_ch = rev_encrypt(roter2, en_ch)
            en_ch = rev_encrypt(roter1, en_ch)
            en_ch = apply_plugboard(en_ch)
            encrypt_msg += en_ch
            encriptMsg = encrypt_msg.upper()
        else:
            encrypt_msg += ch
            encriptMsg = encrypt_msg.upper()
    result_text.delete("1.0", "end")
    result_text.insert("1.0", encriptMsg)

def decrypt_message():
    global encriptMsg
    global decrypt_text
    encrypt_msg = decrypt_text.get("1.0", "end-1c")
    decrypt_msg = ""
    initial_setup()
    for ch in encrypt_msg:
        if ch.isalpha():
            rotate_roters()
            ch = apply_plugboard(ch)
            en_ch = encrypt_roter(roter1, ch)
            en_ch = encrypt_roter(roter2, en_ch)
            en_ch = encrypt_roter(roter3, en_ch)
            en_ch = reflect(en_ch)
            en_ch = rev_encrypt(roter3, en_ch)
            en_ch = rev_encrypt(roter2, en_ch)
            en_ch = rev_encrypt(roter1, en_ch)
            en_ch = apply_plugboard(en_ch)
            decrypt_msg += en_ch
            encriptMsg = decrypt_msg.upper()
        else:
            decrypt_msg += ch
            encriptMsg = decrypt_msg.upper()
    result_text.delete("1.0", "end")
    result_text.insert("1.0", encriptMsg)

def encrypt_roter(roter, ch):
    ch_index = ord(ch.upper()) - 65
    if ch.islower():
        return roter[ch_index].lower()
    else:
        return roter[ch_index]

def reflect(ch):
    if ch.upper() in reflector[0]:
        index = reflector[0].index(ch.upper())
        if ch.islower():
            return reflector[1][index].lower()
        else:
            return reflector[1][index]
    else:
        index = reflector[1].index(ch.upper())
        if ch.islower():
            return reflector[0][index].lower()
        else:
            return reflector[0][index]

def rev_encrypt(roter, ch):
    ch_index = roter.index(ch.upper())
    if ch.islower():
        ch_found = chr(97 + ch_index)
    else:
        ch_found = chr(65 + ch_index)
    return ch_found

def apply_plugboard(ch):
    for pair in plugboard_pairs:
        if ch.upper() == pair[0]:
            return pair[1]
        elif ch.upper() == pair[1]:
            return pair[0]
    return ch

def open_plugboard_window():
    plugboard_window = tk.Toplevel(root)
    plugboard_window.title("Plugboard Setup")
    plugboard_window.configure(bg='#F0F0F0')

    plugboard_label = tk.Label(plugboard_window, text="Enter plugboard pairs (e.g., AB CD EF):", font=('Arial', 12), bg='#F0F0F0')
    plugboard_label.pack()

    plugboard_entry = tk.Entry(plugboard_window, font=('Arial', 12))
    plugboard_entry.pack()

    def set_plugboard_pairs():
        global plugboard_pairs
        pairs_str = plugboard_entry.get()
        pairs_str = pairs_str.upper()
        pairs_list = pairs_str.split(" ")
        for pair in pairs_list:
            if len(pair) == 2 and pair[0].isalpha() and pair[1].isalpha():
                plugboard_pairs.append(pair)
        plugboard_window.destroy()

    plugboard_button = ttk.Button(plugboard_window, text="Set Plugboard", style='Custom.TButton', command=set_plugboard_pairs)
    plugboard_button.pack()

root = tk.Tk()
root.title("Enigma Machine")
root.geometry("500x500")  
root.configure(bg='#F0F0F0')  

encrypt_label = tk.Label(root, text="Enter message to be encrypted:", font=('Arial', 12), bg='#F0F0F0')
encrypt_label.pack(pady=10)

encrypt_text = tk.Text(root, height=5, width=50, font=('Arial', 12))
encrypt_text.pack()

encrypt_button = ttk.Button(root, text="Encrypt", style='Custom.TButton', command=encrypt_message)
encrypt_button.pack(pady=10)

decrypt_label = tk.Label(root, text="Enter message to be decrypted:", font=('Arial', 12), bg='#F0F0F0')
decrypt_label.pack(pady=10)

decrypt_text = tk.Text(root, height=5, width=50, font=('Arial', 12))
decrypt_text.pack()

decrypt_button = ttk.Button(root, text="Decrypt", style='Custom.TButton', command=decrypt_message)
decrypt_button.pack(pady=10)

result_label = tk.Label(root, text="Result:", font=('Arial', 12), bg='#F0F0F0')
result_label.pack()

result_text = tk.Text(root, height=5, width=50, font=('Arial', 12))
result_text.pack()

plugboard_button = ttk.Button(root, text="Plugboard Setup", style='Custom.TButton', command=open_plugboard_window)
plugboard_button.pack(pady=10)

style = ttk.Style()
style.configure('Custom.TButton', font=('Arial', 12))

prototype_label = tk.Label(root, text="ENIGMA MACHINE PROTOTYPE", font=('Arial', 16, 'bold'), bg='#F0F0F0')
prototype_label.pack(pady=10)

author_label = tk.Label(root, text="Made by Nawang Dorjay", font=('Arial', 12), bg='#F0F0F0')
author_label.pack(pady=5)

root.mainloop()