from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    letters_list = [choice(letters) for char in range(nr_letters)]
    symbols_list = [choice(symbols) for char in range(nr_symbols)]
    numbers_list = [choice(numbers) for char in range(nr_numbers)]
    password_list = letters_list + symbols_list + numbers_list

    shuffle(password_list)

    password = "".join(password_list)

    pw_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = web_entry.get().title()
    email = email_entry.get()
    pw = pw_entry.get()
    new_info = {
        web: {
            "email":email,
            "password":pw,
         }
    }

    if len(web) == 0 or len(email) == 0 or len(pw) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askyesno(title=web, message=f"These are the details entered: \nEmail: {email} \nPassword: {pw}\nIs it "
                                                f"ok to save?")
        if is_ok == True:
            try:
                with open("data.json", "r") as f:
                    #Reading old data
                    info = json.load(f)

            except FileNotFoundError:
                with open("data.json", "w") as f:
                    json.dump(new_info, f, indent=4)

            else:
                # Updating old data with new data
                info.update(new_info)
                with open("data.json", "w") as f:
                    #Saving the updated data
                    json.dump(info, f, indent=4)

            finally:
                web_entry.delete(0, END)
                email_entry.delete(0, END)
                pw_entry.delete(0, END)
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    web = web_entry.get().title()
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
    else:
        for key in data:
            if web == key:
                messagebox.showinfo(title=f"{key}", message=f"Email: {data[key]['email']}\nPassword:{data[key]['password']}")
            else:
                messagebox.showinfo(title= "Sorry", message="No details for the website exists.")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

web_label = Label(text="Website:")
web_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
pw_label = Label(text="Password:")
pw_label.grid(row=3, column=0)

web_entry = Entry(width=21)
web_entry.focus()
web_entry.grid(row=1, column=1, sticky="EW")
email_entry = Entry(width=35)
email_entry.insert(0, "james@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
pw_entry = Entry(width=21)
pw_entry.grid(row=3, column=1, sticky="EW")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, sticky="EW")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")
search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()