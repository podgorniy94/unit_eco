from math import ceil
from tkinter import messagebox

import customtkinter as cttk
import requests
from pyperclip import copy

from calc_cargo import create_table, dec_number, read_cargo_data

cttk.set_appearance_mode("light")
cttk.set_default_color_theme("dark-blue")

win = cttk.CTk()
win.title("Unit Economics")
win.geometry("660x640")
win.grid_columnconfigure((0, 1, 2), weight=1)


# --- Main Logic
def create_label(text, row, column):
    cttk.CTkLabel(win, text=text, anchor="w").grid(
        row=row, column=column, sticky="we", padx=(25, 0)
    )


def create_bt():
    return cttk.CTkButton(
        win, text=" ", fg_color="#e8e8e8", text_color="black", hover_color="#bababa"
    )


def place_bt(bt, row, column):
    bt.grid(row=row, column=column, padx=(25, 0), sticky="we")
    bt.configure(command=lambda: copy_to_clip(bt.cget("text")))


def create_entry():
    return cttk.CTkEntry(win)


def place_entry(entry, row, column):
    entry.grid(row=row, column=column, padx=(25, 0), sticky="we")
    entry.bind("<FocusIn>", lambda event: clean(entry))


def clean(field):
    value = field.get()
    if value == mandatory or value == not_digit or value == int_notif or value == "0":
        field.configure(text_color="black")
        field.delete(0, cttk.END)


def copy_to_clip(text):
    if text:
        copy(text[:-2])
        messagebox.showinfo("Успех", "Скопировано")


def add_bt_text(bt, value):
    bt.configure(text=f"{dec_number(round(value, 2))} ¥")


def get_curr():
    url = "https://api.freecurrencyapi.com/v1/latest"
    api_key = "fca_live_CKKpxzepp3RFgAQJD6EPR7TdYphkAwRkO9C6sLOQ"
    currencies = "CNY"

    params = {"apikey": api_key, "currencies": currencies}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        json_data = response.json()["data"]
        curr_var.set(round(json_data["CNY"], 2))


int_notif = "Введите целое число"


def is_int(entry):
    try:
        int(entry.get())
        return True
    except ValueError:
        entry.delete(0, cttk.END)
        entry.insert(0, int_notif)
        entry.configure(text_color="red")
        return False


# --- Calculation
def calculate():
    if validate():
        if is_int(prod_amount) and is_int(amount_in_box):
            density, total_volume, total_weight = calc_density()
            log = calc_log(density, total_volume, total_weight)
            calc_totals(total_volume, log)


def calc_density():
    box_amount = ceil(int(prod_amount.get()) / int(amount_in_box.get()))
    origin_weight = box_amount * float(box_weight.get())
    demension = float(height.get()) * float(width.get()) * float(length.get())
    volume = demension * box_amount / 1000000
    total_weight = ceil(origin_weight + (volume / 2 * 50))
    total_volume = volume + (volume / 2 * 0.5)
    density = total_weight / total_volume

    return density, total_volume, total_weight


def calc_log(density, total_volume, total_weight):
    if density >= 100:
        cargo_dict, discount = read_cargo_data()
        max_den = max(filter(lambda k: int(k) <= density, cargo_dict.keys()), key=int)
        cargo_coeff = float(cargo_dict[max_den]) - discount
        log_price = cargo_coeff * total_weight * curr_var.get()
    else:
        log_price = float(density) * total_volume

    return log_price


def calc_totals(total_volume, log_price):
    goods_cost_val = float(price.get()) * int(prod_amount.get())
    add_bt_text(goods_cost_bt, goods_cost_val)

    package_val = total_volume * 210
    add_bt_text(package_bt, package_val)

    insurance_val = goods_cost_val / 100
    add_bt_text(insurance_bt, insurance_val)

    total_cost_val = goods_cost_val + package_val + log_price + insurance_val
    add_bt_text(total_cost_bt, total_cost_val)

    one_goods_val = total_cost_val / int(prod_amount.get())
    add_bt_text(one_goods_bt, one_goods_val)

    add_bt_text(log_bt, log_price)


mandatory = "Обязательное поле"
not_digit = "Нечисловое значение"
digits_seps = "0123456789,."


def validate():
    win.focus_set()
    valid = 1

    for field in fields:
        value = field.get()

        if "," in value:
            upd_val = value.replace(",", ".")
            field.delete(0, cttk.end)
            field.insert(0, upd_val)

        if not value:
            field.insert(0, mandatory)
            field.configure(text_color="red")
            valid = 0
        elif value == mandatory or value == int_notif or value == not_digit:
            valid = 0
            continue
        elif value == not_digit:
            field.delete(0, cttk.END)
            field.insert(0, mandatory)
            valid = 0
        elif not all(digit in digits_seps for digit in value):
            field.delete(0, cttk.END)
            field.insert(0, not_digit)
            field.configure(text_color="red")
            valid = 0
        elif value == "0":
            field.delete(0, cttk.END)
            field.insert(0, "0")
            field.configure(text_color="red")
            valid = 0
    return valid


# --- Params
create_label("Товар", 0, 0)
product = create_entry()
place_entry(product, 1, 0)

create_label("Цена в Китае", 0, 1)
price = create_entry()
place_entry(price, 1, 1)

create_label("Количество", 0, 2)
prod_amount = create_entry()
place_entry(prod_amount, 1, 2)

create_label("Высота", 2, 0)
height = create_entry()
place_entry(height, 3, 0)

create_label("Ширина", 2, 1)
width = create_entry()
place_entry(width, 3, 1)

create_label("Длина", 2, 2)
length = create_entry()
place_entry(length, 3, 2)

create_label("Кол. шт. в коробке", 4, 0)
amount_in_box = create_entry()
place_entry(amount_in_box, 5, 0)

create_label("Вес", 4, 1)
box_weight = create_entry()
place_entry(box_weight, 5, 1)


curr_var = cttk.DoubleVar(value=7.25)
get_curr()  # --- Getting latest USD/CNY currency
create_label("Курс $/¥ ", 4, 2)
currency = cttk.CTkEntry(win, textvariable=curr_var)
place_entry(currency, 5, 2)


# --- Calculation result

create_label("Стоимость товара", 6, 0)
goods_cost_bt = create_bt()
place_bt(goods_cost_bt, 7, 0)

create_label("Упаковка", 6, 1)
package_bt = create_bt()
place_bt(package_bt, 7, 1)

create_label("Страховка", 6, 2)
insurance_bt = create_bt()
place_bt(insurance_bt, 7, 2)

create_label("Стоимость груза", 8, 0)
total_cost_bt = create_bt()
place_bt(total_cost_bt, 9, 0)

create_label("За единицу", 8, 1)
one_goods_bt = create_bt()
place_bt(one_goods_bt, 9, 1)

create_label("Логистика", 8, 2)
log_bt = create_bt()
place_bt(log_bt, 9, 2)


fields = [price, prod_amount, height, width, length, amount_in_box, box_weight]

cttk.CTkButton(win, text="Рассчитать", command=calculate).grid(
    row=15, column=1, sticky="wens", pady=10, padx=(25, 0)
)

# --- Creating cargo table
create_table(win, cttk)

win.mainloop()