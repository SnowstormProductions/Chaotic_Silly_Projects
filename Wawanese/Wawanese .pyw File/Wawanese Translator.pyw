import tkinter as tk
import pyperclip

blist = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    ":",
    ";",
    "\"",
    "\\",
    "/",
    ",",
    ".",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    "\'",
    "+",
    "-",
    "=",
    "`",
    "~",
    ">",
    "<",
    "?",
    "…",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "∞",
    "™",
    "\n",
    "\t",
    "⁰",
    "¹",
    "²",
    "³",
    "⁴",
    "⁵",
    "⁶",
    "⁷",
    "⁸",
    "⁹",
    "ⁿ",
    "ⁱ",
    "⁺",
    "⁻",
    "⁼",
    "|",
    "π",
    "░",
    "▒",
    "▓",
    "█",
    "©",
    "®",
    "°",
    "ƒ",
    "×",
    "«",
    "»",
    "÷",
    "Ø"
]
print(len(blist))
a = {}
def dothis(yep, word):
    return (word[0].lower() if yep[0] == "0" else word[0].upper()) + (word[1].lower() if yep[1] == "0" else word[1].upper()) + (word[2].lower() if yep[2] == "0" else word[2].upper()) + (word[3].lower() if yep[3] == "0" else word[3].upper())

for i in range(len(blist)):
    b = bin(i % 16)[2:]
    a[blist[i]] = dothis((4 - len(b)) * "0" + b, ["wawa", "waaa", "waww", "wwaa", "waaw", "aaaw", "awaw", "aaww", "awaa", "aawa", "wwaw", "wwwa"][i // 16])
a[" "] = " "

for k, v in a.items():
    print(f"{k}: {v}")


reva = {}
for k, v in a.items():
    reva[v] = k

def decode(string):
    decoded = ""
    char = ""
    s = 0
    for i in string:
        if i in [" ", "\n", "\t"]:
            decoded += i
            s = 0
            char = ""
        else:
            char += i
            s += 1
            if s >= 4:
                s = 0
                decoded += reva[char]
                char = ""
            
    return decoded


def encode(string):
    newmes = ""
    for ip, i in enumerate(string):
        if i in [" ", "\n", "\t"]:
            newmes += i
        else:
            try:
                newmes += a[i]
            except KeyError:
                print(f"ugh error for {i}")
    return newmes
    

window = tk.Tk()
window.title("Wawanese Translator")

bg_color = "#F3E0AC"
input_bg_color = "#FFEFDC"

version_label = tk.Label(window, text="Version: 1.0.0", fg="light gray")
version_label.place(x=10, y=0)

input_label = tk.Label(window, text="English")
input_label.grid(row=0, column=0, padx=10, pady=5)

input_textbox = tk.Text(window, height=10, width=30, bg=input_bg_color)
input_textbox.grid(row=1, column=0, padx=10, pady=5)

output_label = tk.Label(window, text="Wawanese")
output_label.grid(row=0, column=1, padx=10, pady=5)

output_textbox = tk.Text(window, height=10, width=30, bg=input_bg_color)
output_textbox.grid(row=1, column=1, padx=10, pady=5)

def encode_text():
    english_text = input_textbox.get("1.0", "end-1c")
    encoded_text = encode(english_text)
    output_textbox.delete("1.0", "end")
    output_textbox.insert("1.0", encoded_text)

def decode_text():
    slugcipher_text = output_textbox.get("1.0", "end-1c")
    decoded_text = decode(slugcipher_text)
    input_textbox.delete("1.0", "end")
    input_textbox.insert("1.0", decoded_text)

def copy_english_text():
    english_text = input_textbox.get("1.0", "end-1c")
    pyperclip.copy(english_text)

def copy_slugcipher_text():
    slugcipher_text = output_textbox.get("1.0", "end-1c")
    pyperclip.copy(slugcipher_text)

encode_button = tk.Button(window, text="Encode", command=encode_text)
encode_button.grid(row=2, column=0, pady=10, padx=10)

decode_button = tk.Button(window, text="Decode", command=decode_text)
decode_button.grid(row=2, column=1, pady=10, padx=10)

copy_english_button = tk.Button(window, text="Copy", command=copy_english_text)
copy_english_button.grid(row=3, column=0, pady=5, padx=10)

copy_slugcipher_button = tk.Button(window, text="Copy", command=copy_slugcipher_text)
copy_slugcipher_button.grid(row=3, column=1, pady=5, padx=10)

window.mainloop()
