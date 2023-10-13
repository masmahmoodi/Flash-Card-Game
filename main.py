import random
from tkinter import *
from tkinter import PhotoImage
from pandas import *
BACKGROUND_COLOR = "#B1DDC6"
current_choice = {}
to_learn = {}
try:
    data = read_csv("data/should_learn.csv")
except FileNotFoundError:
    original_data = read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")

else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_choice, flip_timer
    window.after_cancel(flip_timer)
    current_choice = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_choice["French"], fill="black")
    canvas.itemconfig(card_img, image=img_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_img, image=img_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_choice["English"], fill="white")


def is_known():
    to_learn.remove(current_choice)
    words_should_learn = DataFrame(to_learn)
    words_should_learn.to_csv("data/should_learn.csv",index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
img_front = PhotoImage(file="images/card_front.png")
img_back = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(400, 263, image=img_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 50, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
img_wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=img_wrong, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

img_right = PhotoImage(file="images/right.png")
right_button = Button(image=img_right, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
