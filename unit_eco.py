import tkinter as tk
from math import ceil
from tkinter import messagebox

from pyperclip import copy

win = tk.Tk()
win.title("Unit Economics")
win.geometry("500x270")

# --- Логика


def int_r(num):
    num = int(float(num) + 0.5)
    return num


def clean(field):
    value = field.get()
    field["fg"] = "black"
    if value == mandatory or value == not_digit:
        field.delete(0, tk.END)


def copy_to_clip(text):
    if text:
        copy(text)
        messagebox.showinfo("Успех", "Скопировано")


mandatory = "Обязательное поле"
not_digit = "Нечисловое значение"


def validate():
    win.focus_set()
    valid = 1
    for field in fields:
        if not field.get():
            field.insert(0, mandatory)
            field["fg"] = "red"
            valid = 0

        elif field.get() == mandatory:
            valid = 0
            continue

        elif field.get() == not_digit:
            field.delete(0, tk.END)
            field.insert(0, mandatory)
            valid = 0

        elif not field.get().isdigit():
            field.delete(0, tk.END)
            field.insert(0, not_digit)
            field["fg"] = "red"
            valid = 0
        else:
            field["fg"] = "black"

    return valid


def calculate():
    if validate():
        box_amount = ceil(int(prod_amount.get()) / int(amount_in_box.get()))
        total_weight = box_amount * float(box_weight.get())
        volume = (
            int_r(height.get())
            * int_r(width.get())
            * int_r(length.get())
            * box_amount
            / 1000000
        )
        total_weight = ceil(total_weight + (volume / 2 * 50))
        total_volume = volume + (volume / 2 * 0.5)
        density = round(total_weight / total_volume, 2)

        log = calc_log(density, total_volume, total_weight)
        count_total(total_volume, log)


def count_total(total_volume, log):
    goods_cost = float(price.get()) * int(prod_amount.get())
    goods_cost_bt["text"] = f"{round(goods_cost, 2)} ¥"

    package = total_volume * 210
    package_bt["text"] = f"{round(package, 2)} ¥"

    insurance = goods_cost / 100
    insurance_bt["text"] = f"{insurance} ¥"

    total_cost = goods_cost + package + log + insurance
    total_cost_bt["text"] = f"{round(total_cost, 2)} ¥"

    one_goods = total_cost / int(prod_amount.get())
    one_goods_bt["text"] = f"{round(one_goods, 2)} ¥"


def calc_log(density, total_volume, total_weight):
    log = (
        (cargo_dict[max(filter(lambda x: x <= density, cargo_dict.keys()))] - discount)
        * total_weight
        * 7.25
        if density >= 100
        else 600 * total_volume
    )
    log_bt["text"] = f"{round(log, 2)} ¥"
    return log


# --- Параметры

tk.Label(win, text="Товар").grid(row=0, column=0, sticky="w")
product = tk.Entry(win)
product.grid(row=1, column=0)

tk.Label(win, text="Цена").grid(row=0, column=1, sticky="w")
price = tk.Entry(win)
price.bind("<FocusIn>", lambda event: clean(price))
price.grid(row=1, column=1)

tk.Label(win, text="Количество").grid(row=0, column=2, sticky="w")
prod_amount = tk.Entry(win)
prod_amount.bind("<FocusIn>", lambda event: clean(prod_amount))
prod_amount.grid(row=1, column=2)

tk.Label(win, text="Высота").grid(row=2, column=0, sticky="w")
height = tk.Entry(win)
height.bind("<FocusIn>", lambda event: clean(height))
height.grid(row=3, column=0)

tk.Label(win, text="Ширина").grid(row=2, column=1, sticky="w")
width = tk.Entry(win)
width.bind("<FocusIn>", lambda event: clean(width))
width.grid(row=3, column=1)

tk.Label(win, text="Длина").grid(row=2, column=2, sticky="w")
length = tk.Entry(win)
length.bind("<FocusIn>", lambda event: clean(length))
length.grid(row=3, column=2)

tk.Label(win, text="Кол. шт. в коробке").grid(row=4, column=0, sticky="w")
amount_in_box = tk.Entry(win)
amount_in_box.bind("<FocusIn>", lambda event: clean(amount_in_box))
amount_in_box.grid(row=5, column=0)

tk.Label(win, text="Вес").grid(row=4, column=1, sticky="w")
box_weight = tk.Entry(win)
box_weight.bind("<FocusIn>", lambda event: clean(box_weight))
box_weight.grid(row=5, column=1)

fields = [price, prod_amount, height, width, length, amount_in_box, box_weight]

tk.Button(win, text="Рассчитать", command=calculate).grid(
    row=4, column=2, sticky="wens", rowspan=2, pady=3, padx=3
)

# --- Рассчет

tk.Label(win, text="Стоимость товара").grid(row=6, column=0, sticky="w", padx=3)
goods_cost_bt = tk.Button(win, state=tk.DISABLED)
goods_cost_bt.grid(row=7, column=0, sticky="we", padx=3)

tk.Label(win, text="Упаковка").grid(row=6, column=1, sticky="w", padx=3)
package_bt = tk.Button(win, state=tk.DISABLED)
package_bt.grid(row=7, column=1, sticky="we", padx=3)

tk.Label(win, text="Страховка").grid(row=6, column=2, sticky="w", padx=3)
insurance_bt = tk.Button(win, state=tk.DISABLED)
insurance_bt.grid(row=7, column=2, sticky="we", padx=3)

tk.Label(win, text="Стоимость груза").grid(row=8, column=0, sticky="w", padx=3)
total_cost_bt = tk.Button(win)
total_cost_bt["command"] = lambda: copy_to_clip(total_cost_bt["text"])
total_cost_bt.grid(row=9, column=0, sticky="we", padx=3)

tk.Label(win, text="За штуку").grid(row=8, column=1, sticky="w", padx=3)
one_goods_bt = tk.Button(win, state=tk.DISABLED)
one_goods_bt.grid(row=9, column=1, sticky="we", padx=3)

tk.Label(win, text="Логистика").grid(row=8, column=2, sticky="w", padx=3)
log_bt = tk.Button(win, state=tk.DISABLED)
log_bt.grid(row=9, column=2, sticky="we", padx=3)

win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)
win.grid_columnconfigure(2, weight=1)

discount = 0.2
cargo_dict = {
    400: 2.2,
    350: 2.3,
    300: 2.4,
    200: 2.5,
    190: 2.6,
    180: 2.7,
    170: 2.8,
    160: 2.9,
    150: 3,
    140: 3.1,
    130: 3.2,
    120: 3.3,
    110: 3.4,
    100: 3.5,
}

win.mainloop()
