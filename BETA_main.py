import random
import time
from tkinter import *
import pandas
from random import *

# Global variables
background = "#343434"
flash_card_font = "Ariel"
current_index = 0
current_text = ""
answering = False  # Used to avoid the functions getting called multiple times while still answering.
finished = False
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


# ----------------------------------------# FUNCTIONS #-------------------------------------------#


def edit_text(side):
    """edits the text in the flashcard."""
    if side == "front":
        canvas.itemconfig(can_word, text=word_list[current_index]["French"], fill="black")
        canvas.itemconfig(can_lang, text="French", fill="black")
        canvas.itemconfig(card_background, image=front)
    elif side == "back":
        canvas.itemconfig(can_lang, text="ENGLISH", fill="white")
        canvas.itemconfig(can_word, text=current_text, fill="white")
        canvas.itemconfig(card_background, image=back)


def new_word():
    """Gets a random index for the word_list, and calls the function edit_text."""
    global current_index, flip_timer, current_text, answering
    if not answering and not finished:  # Only continues if not answering and not finished.
        answering = True
        window.after_cancel(flip_timer)
        current_index = randint(0, len(word_list) - 1)
        edit_text("front")
        current_text = word_list[current_index]["English"]
        flip_timer = window.after(3000, func=flip_card)


def delete():
    """If there is less than one item in the list,
     returns completed. calls the new word function,
    deletes the item in the list."""
    global answering, word_list
    if not answering and not finished:  # Only continues if not answering and not finished.
        if len(word_list) < 1:
            return completed()
        new_word()
        del word_list[current_index]
        list_count_label.config(text=f"Words Left: {len(word_list)}")  # Edits the words left count.


def flip_card():
    """Flips the card to show the answer."""
    global current_index, current_text, answering
    if answering:  # Checks if answering to prevent unwanted editing from flip_timer.
        edit_text("back")
        answering = False


def completed():
    """Tells the user that all the flashcards are completed
    when word_list is empty. """
    global finished
    finished = True
    canvas.itemconfig(can_lang, text="")
    canvas.itemconfig(can_word, text="YOU HAVE COMPLETED\nALL THE FLASHCARDS!", fill="black")
    canvas.itemconfig(card_background, image=front)


flip_timer = window.after(3000, func=flip_card)
# --------------------------------------# CANVAS #---------------------------------------------#

canvas = Canvas(width=500, height=250, background=background, highlightthickness=0)
front = PhotoImage(file="front.png")
back = PhotoImage(file="back.png")
card_background = canvas.create_image(250, 125, image=front)
can_lang = canvas.create_text(250, 50, text="FRENCH", font=(flash_card_font, 16, "italic"))
can_word = canvas.create_text(250, 130, text="WORD", font=(flash_card_font, 20, "bold"))
canvas.place(x=5, y=5)

# --------------------------------------# BUTTONS #--------------------------------------------#

x_image = PhotoImage(file="x_mark.png")
x_button = Button(image=x_image, background=background, height=30, width=30, command=new_word)
x_button.place(x=100, y=280)

check_image = PhotoImage(file="check_mark.png")
check_button = Button(image=check_image, background=background, height=30, width=30, command=delete)
check_button.place(x=380, y=280)

list_count_label = Label(text=f"Words Left: {len(word_list)}", bg=background, fg="white", font=("Ariel", 12, "bold"))
list_count_label.place(x=50, y=-30)

window.mainloop()
