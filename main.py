from tkinter import *
from random import *
from tkinter import messagebox
from pw_lists import *
import pyperclip
import json

FONT_SIZE = 12

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pw(p_input):
    letter_list = [choice(letters) for i in range(randint(6, 10))]
    num_list = [choice(numbers) for j in range(randint(5, 7))]
    symbol_list = [choice(symbols) for k in range(randint(5, 7))]

    combined_list = letter_list + num_list + symbol_list
    shuffle(combined_list)
    final_password = ''.join(combined_list)

    if len(p_input.get()) > 0:
        p_input.delete(0, END)

    p_input.insert(index=0, string=final_password)

# -------------------------- SEARCH PASSWORD ------------------------------- #

def find_password(s_input, u_input):
    my_site = s_input.get()
    my_email = u_input.get()
    if len(my_site) == 0 or len(my_email) == 0:
        messagebox.showwarning(title="Entry Error", message="Please fill in all required fields and try again.")
    else:
        try:
            with open("data.json", mode="r") as desired_data:
                j_data = json.load(desired_data)
                desired_pw = j_data[my_site]["Password: "]
        except FileNotFoundError:
            messagebox.showwarning(title="No Data", message="You do not have any data yet.")
        except KeyError:
            messagebox.showwarning(title="Website Not Found", message="You do not have a password with this website.")
        else:
            pyperclip.copy(desired_pw)
            messagebox.showinfo(title="Password Found",
                                message=f"Password found with {my_site}.\nRegistered with {my_email}."
                                        "\n\nPassword copied to clipboard.")

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save(s_input, u_input, p_input):
    site = s_input.get()
    username = u_input.get()
    password = p_input.get()
    new_data = {
        site: {
            "Email: ": username,
            "Password: ": password
        }
    }

    if len(site) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Entry Error", message="Please fill in all required fields and try again.")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            pyperclip.copy(password)
            s_input.delete(0, END)
            p_input.delete(0, END)
            messagebox.showinfo(title="Confirmation", message="Password copied to clipboard.")

# -------------------------- SEARCH PASSWORD ------------------------------- #

def delete_pw(s_input, u_input):
    my_site = s_input.get()
    my_email = u_input.get()

    if len(my_site) == 0 or len(my_email) == 0:
        messagebox.showwarning(title="Entry Error", message="Please fill in all required fields and try again.")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                del data[my_site]
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        except FileNotFoundError:
            messagebox.showwarning(title="No Data",message="You do not have any data yet.")
        except KeyError:
            messagebox.showwarning(title="Entry Error", message="You do not have a password with this website.")
        else:
            messagebox.showinfo(title="Deleted", message="Password deleted.")
            s_input.delete(0, END)
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
my_canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")

my_canvas.create_image(100, 100, image=logo)
my_canvas.grid(column=1, row=0)

site_label = Label(text="Website: ", font=("Arial", FONT_SIZE))
site_label.grid(column=0, row=1, pady=3)

site_input = Entry(width=30)
site_input.grid(column=1, row=1, columnspan=2, sticky=W, pady=3)
site_input.focus()

email_label = Label(text="Email/Username: ", font=("Arial", FONT_SIZE))
email_label.grid(column=0, row=2, pady=3)

email_input = Entry(width=30)
email_input.insert(index=0, string="jrydel92@gmail.com")
email_input.grid(column=1, row=2, columnspan=2, sticky=W, pady=3)

pw_label = Label(text="Password: ", font=("Arial", FONT_SIZE))
pw_label.grid(column=0, row=3, pady=3)

pw_input = Entry(width=30)
pw_input.grid(column=1, row=3, sticky=W, pady=3)

pw_button = Button(text="Generate Password", width=15, command=lambda: generate_pw(pw_input))
pw_button.grid(column=2, row=3, sticky=W, pady=3)

add_button = Button(text="Add", width=44, command=lambda: save(site_input, email_input, pw_input))
add_button.grid(column=1, row=4, columnspan=2, sticky=W, pady=5)

search_button = Button(text="Search", width=15, command=lambda: find_password(site_input, email_input))
search_button.grid(column=2, row=1, sticky=W, pady=3)

del_button = Button(text="Delete Password", width=15, command=lambda: delete_pw(site_input, email_input))
del_button.grid(column=2, row=2, sticky=W, pady=3)

window.mainloop()
