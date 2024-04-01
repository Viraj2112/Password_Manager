from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import math
import json

# CONSTANTS:-
PASSWORD_LENGTH = 10
NUM_NUMBERS = 0
NUM_SYMBOLS = 0
NUM_CAP_LETTERS = 0
NUM_SMALL_LETTERS = 0
INCLUDE_NUMBERS = 0
INCLUDE_SYMBOLS = 0


def set_password_length(value):
    global PASSWORD_LENGTH
    PASSWORD_LENGTH = int(value)


def include_caps_letter():
    global NUM_CAP_LETTERS
    if checked_state_1.get() == 1:
        if checked_state_2.get() == 0:
            NUM_CAP_LETTERS = int(PASSWORD_LENGTH) - int(NUM_SYMBOLS) - int(NUM_NUMBERS)
        else:
            NUM_CAP_LETTERS = math.floor((int(PASSWORD_LENGTH) - int(NUM_SYMBOLS) - int(NUM_NUMBERS)) / 2)
    else:
        NUM_CAP_LETTERS = 0


def include_small_letter():
    global NUM_SMALL_LETTERS
    if checked_state_2.get() == 1:
        if checked_state_1.get() == 0:
            NUM_SMALL_LETTERS = int(PASSWORD_LENGTH) - int(NUM_SYMBOLS) - int(NUM_NUMBERS)
        else:
            NUM_SMALL_LETTERS = math.floor((int(PASSWORD_LENGTH) - int(NUM_SYMBOLS) - int(NUM_NUMBERS)) / 2)
    else:
        NUM_SMALL_LETTERS = 0


def choose_num_numbers():
    global NUM_NUMBERS
    NUM_NUMBERS = int(spinbox_1.get())
    print(NUM_NUMBERS)


def choose_num_symbols():
    global NUM_SYMBOLS
    NUM_SYMBOLS = int(spinbox_2.get())


def include_num():
    global INCLUDE_NUMBERS
    global NUM_NUMBERS
    INCLUDE_NUMBERS = checked_state_3.get()
    if INCLUDE_NUMBERS == 1:
        NUM_NUMBERS = int(spinbox_1.get())
        spinbox_1.config(state='normal')
    else:
        NUM_NUMBERS = 0
        spinbox_1.config(state='disabled')


def include_symbol():
    global INCLUDE_SYMBOLS
    global NUM_SYMBOLS
    INCLUDE_SYMBOLS = checked_state_4.get()
    if INCLUDE_SYMBOLS == 1:
        NUM_SYMBOLS = int(spinbox_2.get())
        spinbox_2.config(state='normal')
    else:
        NUM_SYMBOLS = 0
        spinbox_2.config(state='disabled')


# -------------------------- PASSWORD GENERATOR EXTRA --------------------------- #
def extra_screen():
    window.minsize(730, 380)
    window.config(padx=40, pady=20, bg="#bfeaf2")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

small_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '*', '+']


def generate_password():
    extra_screen()
    global NUM_NUMBERS
    global NUM_SYMBOLS
    include_small_letter()
    include_caps_letter()

    nr_cap_letters = NUM_CAP_LETTERS
    nr_small_letters = NUM_SMALL_LETTERS
    nr_symbols = NUM_SYMBOLS
    nr_numbers = NUM_NUMBERS

    password_list = [random.choice(capital_letters) for _ in range(nr_cap_letters)]
    password_list += [random.choice(small_letters) for _ in range(nr_small_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = ''.join(str(char) for char in password_list)

    pass_generator_entry.delete(0, END)
    pass_generator_entry.insert(0, f"{password}")

    password_entry.delete(0, END)
    password_entry.insert(0, f"{password}")
    pyperclip.copy(password)
    pyperclip.paste()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = website_entry.get().lower()
    paswd = password_entry.get()
    mail = email_entry.get()
    new_data = {
        website: {
            "email": mail,
            "password": paswd,
        }
    }

    if website == "" or mail == "":
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty.")
    elif mail == "Enter your mail":
        messagebox.showwarning(title="Oops", message="You forgot to put your Email.")

    else:
        try:
            with open("data.json", 'r') as file:
                # Reading old Data
                data = json.load(file)
                print("try executed")

        except FileNotFoundError:
            with open("data.json", 'w') as file:
                # Saving updated data
                json.dump(new_data, file, indent=4)
            print("except executed")
        else:
            # Update data of json file
            data.update(new_data)

            with open("data.json", 'w') as file:
                # Saving updated data
                json.dump(data, file, indent=4)
            print("else executed")
        finally:
            delete_entries()


def delete_entries():
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    email_entry.delete(0, END)
    website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.minsize(380, 380)
window.config(padx=20, pady=20, bg="#bfeaf2")

canvas = Canvas(width=200, height=200, bg="#bfeaf2", highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=lock_img)
canvas.grid(row=0, column=1)

# Labels:-
website_label = Label(text="Website:", pady=3, bg="#bfeaf2")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", bg="#bfeaf2")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:", pady=3, bg="#bfeaf2")
password_label.grid(row=3, column=0)

pass_length_label = Label(text="Password Length:", bg="#bfeaf2", pady=3)
pass_length_label.place(x=360, y=80)

pass_generator_label = Label(text="Password Generator", pady=3,
                             bg="#bfeaf2", fg='#d4483b', font=("Aerial", 22, "bold"))
pass_generator_label.place(x=360)

how_many_numbers_label = Label(text="How many numbers ?", pady=3,
                               bg="#bfeaf2", font=("Aerial", 10, "normal"))
how_many_numbers_label.place(x=380, y=250)

how_many_symbols_label = Label(text="How many symbols ?", pady=3,
                               bg="#bfeaf2", font=("Aerial", 10, "normal"))
how_many_symbols_label.place(x=380, y=280)

# Entries:-
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky='w', columnspan=2)
website_entry.focus()

email_entry = Entry(width=39)
email_entry.grid(row=2, column=1, sticky='w', columnspan=2)
email_entry.insert(0, "Enter your mail")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky='w')

pass_generator_entry = Entry(width=25, font=('Aerial', 15, 'bold'),
                             bg='#afb4bd', fg='#0f3987', justify='center', relief='sunken')
pass_generator_entry.place(x=363, y=50)

# Buttons:-
generate_pass_button = Button(text="Generate Password", font=("Aerial", 8, "normal"),
                              relief='groove', command=generate_password)
generate_pass_button.place(x=228, y=247)

add_button = Button(text="Add", width=38, font=("Aerial", 8, "normal"), relief='groove',
                    highlightthickness=2, command=add_password)
add_button.place(x=95, y=274)

clear_button = Button(text="Clear", width=12, font=("Aerial", 8, "normal"), relief='groove',
                      command=delete_entries)
clear_button.place(x=10, y=275)


def find_password():
    website = website_entry.get().lower()
    print(website)
    try:
        with open("data.json", 'r') as file:
            data = json.load(file)
            email = data[website]["email"]
            password = data[website]["password"]
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
        print("No data file found")
    except KeyError:
        messagebox.showerror(title="Error", message="No Details For The Website Exist.")
        print("No data file found")
    else:
        messagebox.showinfo(title=f"{website.title()}", message=f"Email: {email}\nPassword: {password}")


search_button = Button(text="Search", font=("Aerial", 8, "normal"), width=16,
                       relief='groove', command=find_password)
search_button.grid(row=1, column=1, sticky='e', columnspan=2)

# Slider:-
scale = Scale(from_=10, to=18, command=set_password_length,
              orient='horizontal', length=277, bg="#bfeaf2", font=("Aerial", 8, "bold"), highlightthickness=0)
scale.place(x=360, y=105)

# Checkbox:-
checked_state_1 = IntVar()
checkbutton_1 = Checkbutton(text="Use A-Z", variable=checked_state_1, command=include_caps_letter)
# checked_state.get()
checkbutton_1.place(x=390, y=150)

checked_state_2 = IntVar()
checkbutton_2 = Checkbutton(text="Use a-z", variable=checked_state_2, command=include_small_letter)
checkbutton_2.place(x=500, y=150)

checked_state_3 = IntVar()
checkbutton_3 = Checkbutton(text="Use 0-9", variable=checked_state_3, command=include_num)
checkbutton_3.place(x=390, y=200)

checked_state_4 = IntVar()
checkbutton_4 = Checkbutton(text="Use !@#$%^&*", variable=checked_state_4, command=include_symbol)
checkbutton_4.place(x=500, y=200)

# Spinbox
spinbox_1 = Spinbox(from_=0, to=4, width=5, state='disabled', command=choose_num_numbers)
spinbox_1.place(x=550, y=254)

spinbox_2 = Spinbox(from_=0, to=4, width=5, state='disabled', command=choose_num_symbols)
spinbox_2.place(x=550, y=280)

window.mainloop()
