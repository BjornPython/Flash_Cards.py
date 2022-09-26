import random
import time
from tkinter import *
import pandas
from random import *

background = "#343434"
flash_card_font = "Ariel"
current_index = 0
current_text = ""
# WINDOW
window = Tk()
window.title("Flash Cards")
window.geometry("600x400")
window.config(padx=50, pady=50, bg=background)

# -----------------------------------------------------------------------------------------------#
# Read FILE
try:
    data = pandas.read_csv("french_words.csv")

except FileNotFoundError:
    print("Cannot find File")
else:
    word_list = (data.to_dict(orient="records"))

test = word_list[:5]


# -----------------------------------------------------------------------------------------------#
# FUNCTIONS


def new_word():
    global current_index, flip_timer, current_text
    window.after_cancel(flip_timer)
    index = randint(0, len(test) - 1)
    canvas.itemconfig(can_word, text=test[index]["French"])
    canvas.itemconfig(can_lang, text="French")
    canvas.itemconfig(card_background, image=front)
    current_index = index
    current_text = test[current_index]["English"]
    print("CURRENT INDEX: ", current_index)
    flip_timer = window.after(3000, func=flip_card)


def delete():
    """If there is less than one item in the list,
     returns completed. calls the new word function,
    deletes the item in the list."""
    if len(test) < 1:
        return completed()
    new_word()
    print("TEST: ", test)
    del test[current_index]
    print("TEST 2: ", test)


def flip_card():
    """Flips the card to show the answer."""
    global current_index, current_text
    canvas.itemconfig(can_lang, text="ENGLISH")
    canvas.itemconfig(can_word, text=current_text)
    canvas.itemconfig(card_background, image=back)


def completed():

    canvas.itemconfig(can_lang, text="")
    canvas.itemconfig(can_word, text="YOU HAVE COMPLETED\nALL THE FLASHCARDS!")
    canvas.itemconfig(card_background, image=front)


flip_timer = window.after(3000, func=flip_card)
# -----------------------------------------------------------------------------------------------#
# CANVAS
canvas = Canvas(width=500, height=250, background=background, highlightthickness=0)
front = PhotoImage(file="front.png")
back = PhotoImage(file="back.png")
card_background = canvas.create_image(250, 125, image=front)
can_lang = canvas.create_text(250, 50, text="FRENCH", font=(flash_card_font, 16, "italic"))
can_word = canvas.create_text(250, 130, text="WORD", font=(flash_card_font, 20, "bold"))
canvas.place(x=5, y=5)

# ----------------------------------------------------------------------------------------------#
# BUTTONS
x_image = PhotoImage(file="x_mark.png")
x_button = Button(image=x_image, background=background, height=30, width=30, command=delete)
x_button.place(x=100, y=280)

check_image = PhotoImage(file="check_mark.png")
check_button = Button(image=check_image, background=background, height=30, width=30, command=new_word)
check_button.place(x=380, y=280)

window.mainloop()
