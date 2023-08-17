from tkinter import *
import pandas
import random
import re

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/list.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Chinese", fill="black")
    canvas.itemconfig(card_pron, text="Pronunciation", fill="black")
    canvas.itemconfig(card_word, text=current_card["Character"], fill="black")
    canvas.itemconfig(card_pron, text=current_card["Pronunciation"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    english_word = current_card["English"]
    new_font_size = 60 if len(english_word) <= 10 else 20
    max_y_coordinate = 270
    
    if len(english_word) > 35:
        # Split the text into chunks of up to 35 characters
        chunks = re.findall(r".{1,35}(?:\W+|$)", english_word)
        formatted_text = "\n".join(chunks)
        canvas.itemconfig(card_word, text=formatted_text, font=("Arial", new_font_size, "bold"), fill="white")
    else:
        canvas.itemconfig(card_word, text=english_word, font=("Arial", new_font_size, "bold"), fill="white")

    canvas.coords(card_word, 400, max_y_coordinate)
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_pron, text="")

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
card_pron = canvas.create_text(400, 200, text="", font=("Ariel", 20, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, border=0, borderwidth=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, border=0, borderwidth=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()



