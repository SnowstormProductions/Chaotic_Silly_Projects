import tkinter as tk
import pyperclip

order = "AaWw"

text_mode = [
    "END",
    "SWITCH",
    "e",
    "t",
    "a",
    "o",
    "i",
    "n",
    "s",
    "h",
    "r",
    "d",
    "l",
    "u",
    "c",
    "m",
    "f",
    "w",
    "g",
    "y",
    "p",
    "b",
    "v",
    "k",
    "x",
    "j",
    "q",
    "z",
    "<",
    ">",
    # first 2 for special
    # first to exit text mod
    # one after first switches to text mode 2
    # space for space
]

text_mode2 = [
    "END",
    "SWITCH",
    "E",
    "T",
    "A",
    "O",
    "I",
    "N",
    "S",
    "H",
    "R",
    "D",
    "L",
    "U",
    "C",
    "M",
    "F",
    "W",
    "G",
    "Y",
    "P",
    "B",
    "V",
    "K",
    "X",
    "J",
    "Q",
    "Z",
    "<",
    ">",
]

fastwords = [
    "wawa",
    "thing",
    "crack",
    "maybe",
    "yeah",
    "kill",
    "that",
    "ther",
    "with",
    "tion",
    "here",
    "ould",
    "ight",
    "have",
    "hich",
    "whic",
    "this",
    "thin",
    "they",
    "atio",
    "ever",
    "from",
    "ough",
    "were",
    "hing",
    "ment",
    "when",
    "then",
    "deez",
    "nuts",
    "the",
    "and",
    "ing",
    "her",
    "hat",
    "his",
    "tha",
    "ere",
    "for",
    "ent",
    "ion",
    "ter",
    "was",
    "you",
    "ith",
    "ver",
    "all",
    "wit",
    "thi",
    "tio",
    "why",
    "wee",
    "she",
    "my",
    "he",
    "it"
]


def convert_to_int(string: str) -> int:
    return int(string.replace(order[0], "0").replace(order[1], "1").replace(order[2], "2").replace(order[3], "3"), 4)


def convert_to_wawa(num, outlen=4):
    if num == 0:
        return order[0] * outlen
    arr = []
    arr_append = arr.append  # Extract bound-method for faster access.
    _divmod = divmod  # Access to locals is faster.
    base = len(order)
    while num:
        num, rem = _divmod(num, base)
        arr_append(order[rem])
    arr.reverse()
    return order[0] * (outlen - len(arr)) + ''.join(arr)


def closest_to_zero(*args):
    mind = 9999999
    mini = 0
    for i, v in enumerate(args):
        if abs(v) < mind:
            mind = abs(v)
            mini = i
    return args[mini]


def shortest_on_loop(s1: int, s2: int, l: int) -> int:
    return closest_to_zero(s2 - s1, (s2 + l) - s1, (s2 - l) - s1)


def decode(string):
    global newmes, text_offset, mode
    newmes = ""
    mode = "N"
    text_offset = 0
    cursor = 0
    print("started decoding")
    while cursor < len(string):
        remains = string[cursor:]
        # (remains)
        i = remains[0]
        if mode == "N":
            if i == order[0]:
                mode = order[0]
                text_offset = 0
            elif i == order[1]:
                mode = order[1]
                text_offset = 0
            elif i == order[2]:
                # decoding the word
                word = fastwords[convert_to_int(remains[1:4])]
                cursor += 4
                if string[cursor: cursor + 2] == order[3] + " ":
                    cursor += 2
                    for indx, l in enumerate(string[cursor:cursor + len(word)]):
                        if l == order[0]:
                            newmes += word[indx].upper()
                        else:
                            newmes += word[indx].lower()
                        cursor += 1
                else:
                    newmes += word
                cursor -= 1
            else:
                newmes += i
        elif mode == order[0] or mode == order[1]:
            if i in order:

                txt = text_mode if mode == order[0] else text_mode2

                while remains.startswith(order[0] + " ") or remains.startswith(order[1] + " "):
                    code = string[cursor:cursor + 2]
                    if code == order[0] + " ":
                        text_offset = (text_offset + 8) % len(txt)
                    elif code == order[1] + " ":
                        text_offset = (text_offset - 8) % len(txt)
                    cursor += 2
                    remains = string[cursor:]
                code = string[cursor:cursor + 2]
                offset = convert_to_int(code) - 8
                print(offset, text_offset, sep=", ")
                text_offset = (text_offset + offset) % len(txt)
                text = txt[text_offset]
                cursor += 1
                print(text)
                if text == "SWITCH":
                    text_offset = 0
                    mode = order[0] if mode == order[1] else order[1]
                elif text == "END":
                    text_offset = 0
                    mode = "N"
                else:
                    newmes += text
            else:
                newmes += i
        cursor += 1

    return newmes


def encode(string):
    global newmes, text_offset, mode, order
    newmes = ""
    mode = "N"
    text_offset = 0
    cursor = 0

    def text_type_char(char):
        global newmes, text_offset, mode
        text2 = False if char in text_mode else True if char in text_mode2 else None
        if text2 is None:
            raise "joar"
        if char == "SWITCH":
            text2 = mode == order[1]
        txt = text_mode if char in text_mode else text_mode2 if char in text_mode2 else None

        indx = txt.index(char)
        if mode == "N":
            text_offset = 0
            newmes += order[0] if not text2 else order[1]
        elif text2 and mode == order[0]:
            text_type_char("SWITCH")
        elif not text2 and mode == order[1]:
            text_type_char("SWITCH")
        mode = order[0] if not text2 else order[1]
        offset = shortest_on_loop(text_offset, indx, len(txt))
        print(offset, text_offset, sep=", ")
        print(char)
        newmes += ((order[0] + " ") * (abs(offset) // 8)) if offset > 0 else ((order[1] + " ") * (abs(offset) // 8))
        newmes += convert_to_wawa((offset % 8) + 8 if offset >= 0 else -(abs(offset) % 8) + 8, 2)
        text_offset = indx
        if char == "END" or char == "SWITCH":
            text_offset = 0
    while cursor < len(string):
        remains = string[cursor:]
        i = remains[0]
        used_fw = False
        for wi, w in enumerate(fastwords):
            if remains.startswith(w):
                if mode in [order[0], order[1]]:
                    text_type_char("END")
                    mode = "N"
                newmes += order[2] + convert_to_wawa(wi, 3)
                cursor += len(w) - 1
                used_fw = True
                break
            elif remains.lower().startswith(w.lower()):
                if mode in [order[0], order[1]]:
                    text_type_char("END")
                    mode = "N"
                newmes += order[2] + convert_to_wawa(wi, 3)
                newmes += order[3] + " "
                for p in remains[:len(w)]:
                    if p.isupper():
                        newmes += order[0]
                    else:
                        newmes += order[1]
                cursor += len(w) - 1
                used_fw = True
                break

        if not used_fw:
            if i in text_mode or i in text_mode2:
                text_type_char(i)
            elif i != ">":
                newmes += i

        cursor += 1
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
