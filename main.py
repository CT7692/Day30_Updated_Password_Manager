from tkinter import *
from random import *
from tkinter import messagebox
from pw_lists import *
import pyperclip

FONT_SIZE = 12

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pw(p_input):
    letter_list = [choice(letters) for i in range(randint(5, 7))]
    num_list = [choice(numbers) for j in range(randint(2, 4))]
    symbol_list = [choice(symbols) for k in range(randint(2, 4))]

    combined_list = letter_list + num_list + symbol_list
    shuffle(combined_list)
    final_password = ''.join(combined_list)

    if len(p_input.get()) > 0:
        p_input.delete(0, END)

    p_input.insert(index=0, string=final_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save(s_input, u_input, p_input):
    site = s_input.get()
    username = u_input.get()
    password = p_input.get()

    confirmed = False

    if len(site) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showwarning(title="Entry Error", message="Please fill in all required fields and try again.")
    else:
        confirmed = messagebox.askokcancel(title="Confirmation",
                                           message=f"Website: {site}\nUsername: {username}\nPassword: {password}")
    if confirmed:
        pyperclip.copy(password)
        with open("../../Documents/data.txt", mode="a") as file:
            file.write(f"{site} | {username} | {password}\n")
        s_input.delete(0, END)
        p_input.delete(0, END)
        messagebox.showinfo(title="Confirmation", message="Password copied to clipboard.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
my_canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")

my_canvas.create_image(100, 100, image=logo)
my_canvas.grid(column=1, row=0)

site_label = Label(text="Website: ", font=("Arial", FONT_SIZE))
site_label.grid(column=0, row=1)

site_input = Entry(width=52)
site_input.grid(column=1, row=1, columnspan=2, sticky=W)
site_input.focus()

email_label = Label(text="Email/Username: ", font=("Arial", FONT_SIZE))
email_label.grid(column=0, row=2)

email_input = Entry(width=52)
email_input.insert(index=0, string="jrydel92@gmail.com")
email_input.grid(column=1, row=2, columnspan=2, sticky=W)

pw_label = Label(text="Password: ", font=("Arial", FONT_SIZE))
pw_label.grid(column=0, row=3)

pw_input = Entry(width=27)
pw_input.grid(column=1, row=3, sticky=W)

pw_button = Button(text="Generate Password", command=lambda: generate_pw(pw_input))
pw_button.grid(column=2, row=3, sticky=W)

add_button = Button(text="Add", width=44, command=lambda: save(site_input, email_input, pw_input))
add_button.grid(column=1, row=4, columnspan=2, sticky=W, pady=5)

window.mainloop()