import json
import tkinter as tk
from math import ceil
from tkinter import messagebox, ttk

from pyperclip import copy

win = tk.Tk()
win.title("Unit Economics")
win.geometry("650x600")


# --- Логика
def create_label(text, row, column):
    tk.Label(win, text=text).grid(row=row, column=column, sticky="w", padx=3)


def place_entry(entry, row, column):
    entry.grid(row=row, column=column, padx=3, sticky="we")
    entry.bind("<FocusIn>", lambda event: clean(entry))


def clean(field):
    value = field.get()
    if value == mandatory or value == not_digit or value == integer or value == "0":
        field["fg"] = "black"
        field.delete(0, tk.END)


def place_bt(bt, row, column):
    bt.grid(row=row, column=column, padx=3, sticky="we")
    bt["command"] = lambda: copy_to_clip(bt["text"])


def copy_to_clip(text):
    if text:
        copy(text[:-2])
        messagebox.showinfo("Успех", "Скопировано")


def add_bt_text(bt, value):
    bt["text"] = f"{round(value, 2)} ¥"


integer = "Введите целое число"


def is_int(entry):
    try:
        int(entry.get())
        return True
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(0, integer)
        entry["fg"] = "red"
        return False


# --- Функции для рассчета
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

    return 90, total_volume, total_weight


def calc_log(density, total_volume, total_weight):
    if density >= 100:
        cargo_coeff = cargo_dict[
            max(filter(lambda k: int(k) <= density, cargo_dict.keys()))
        ]
        cargo_coeff = float(cargo_coeff) - discount
        log_price = cargo_coeff * total_weight * 7.25
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
            field.delete(0, tk.END)
            field.insert(0, upd_val)

        if not value:
            field.insert(0, mandatory)
            field["fg"] = "red"
            valid = 0
        elif value == mandatory or value == integer or value == not_digit:
            valid = 0
            continue
        elif value == not_digit:
            field.delete(0, tk.END)
            field.insert(0, mandatory)
            valid = 0
        elif not all(digit in digits_seps for digit in value):
            field.delete(0, tk.END)
            field.insert(0, not_digit)
            field["fg"] = "red"
            valid = 0
        elif value == "0":
            field.delete(0, tk.END)
            field.insert(0, "0")
            field["fg"] = "red"
            valid = 0
    return valid


# --- Параметры

create_label("Товар", 0, 0)
product = tk.Entry(win)
place_entry(product, 1, 0)

create_label("Цена в Китае", 0, 1)
price = tk.Entry(win)
place_entry(price, 1, 1)

create_label("Количество", 0, 2)
prod_amount = tk.Entry(win)
place_entry(prod_amount, 1, 2)

create_label("Высота", 2, 0)
height = tk.Entry(win)
place_entry(height, 3, 0)

create_label("Ширина", 2, 1)
width = tk.Entry(win)
place_entry(width, 3, 1)

create_label("Длина", 2, 2)
length = tk.Entry(win)
place_entry(length, 3, 2)

create_label("Кол. шт. в коробке", 4, 0)
amount_in_box = tk.Entry(win)
place_entry(amount_in_box, 5, 0)

create_label("Вес", 4, 1)
box_weight = tk.Entry(win)
place_entry(box_weight, 5, 1)

# --- Рассчет

create_label("Стоимость товара", 6, 0)
goods_cost_bt = tk.Button(win)
place_bt(goods_cost_bt, 7, 0)

create_label("Стоимость товара", 6, 1)
package_bt = tk.Button(win)
place_bt(package_bt, 7, 1)

create_label("Страховка", 6, 2)
insurance_bt = tk.Button(win)
place_bt(insurance_bt, 7, 2)

create_label("Стоимость груза", 8, 0)
total_cost_bt = tk.Button(win)
place_bt(total_cost_bt, 9, 0)

create_label("За единицу", 8, 1)
one_goods_bt = tk.Button(win)
place_bt(one_goods_bt, 9, 1)

create_label("Логистика", 8, 2)
log_bt = tk.Button(win)
place_bt(log_bt, 9, 2)

# --- Кнопка рассчета

fields = [price, prod_amount, height, width, length, amount_in_box, box_weight]

tk.Button(win, text="Рассчитать", command=calculate).grid(
    row=4, column=2, sticky="wens", rowspan=2, pady=3, padx=3
)

# --- Cargo Таблица

discount = 0.2

with open("cargo_data.json", "r") as file:
    cargo_dict = json.load(file)

no_var = tk.IntVar(value="")
den_var = tk.IntVar(value="")
coeff_var = tk.StringVar(value="")


def item_selected(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        record = item["values"]
        no_var.set(record[0]), den_var.set(record[1])
        coeff_var.set(str(record[2]))
        coeff.focus_set()
        # Record return int if it's not float
        coeff.icursor(len(str(record[2])))


def save_cargo():
    if tree.selection():
        value = coeff.get()
        if "," in value:
            upd_val = value.replace(",", ".")
            coeff.delete(0, tk.END)
            coeff.insert(0, upd_val)

        number = float(coeff.get())
        number = f"{number:.0f}" if number.is_integer() else f"{number}"
        cargo_dict[str(den_var.get())] = str(number)

        with open("cargo_data.json", "w") as file:
            json.dump(cargo_dict, file)

        tree.delete(*tree.get_children())
        load_table(cargo_dict)
        no_var.set(""), den_var.set(""), coeff_var.set("")
        win.focus_set()


def load_table(cargo_dict):
    for i, k in enumerate(cargo_dict):
        tree.insert("", i, text=i + 1, values=(i + 1, k, cargo_dict[k]))


columns = ("No", "Density", "Coeff")
tree = ttk.Treeview(win, columns=columns, show="headings")

item = tree.bind("<<TreeviewSelect>>", item_selected)

tree.grid(row=10, column=0, columnspan=3, sticky="nsew", padx=5, pady=20)
tree.column("No", minwidth=25)
tree.column("Density", minwidth=25)
tree.column("Coeff", minwidth=25)

tree.heading("No", text="No", anchor=tk.CENTER)
tree.heading("Density", text="Плотность", anchor=tk.W)
tree.heading("Coeff", text="Коэффициент", anchor=tk.W)

load_table(cargo_dict)

scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=10, column=3, sticky="nsw", pady=20, padx=5)


tk.Label(win, text="No").grid(row=11, column=0, sticky="w", padx=3)
tk.Label(win, text="Плотность").grid(row=11, column=1, sticky="w", padx=3)
tk.Label(win, text="Коэффициент").grid(row=11, column=2, sticky="w", padx=3)

no = tk.Label(win, borderwidth=1, relief="ridge", textvariable=no_var)
no.grid(row=12, column=0, sticky="we", padx=5)
den = tk.Label(win, borderwidth=1, relief="ridge", textvariable=den_var)
den.grid(row=12, column=1, sticky="we", padx=5)
coeff = tk.Entry(win, textvariable=coeff_var)
coeff.grid(row=12, column=2, sticky="we", padx=5)


tk.Button(win, text="Сохранить", command=save_cargo).grid(
    row=13, column=2, padx=3, sticky="we"
)

win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)
win.grid_columnconfigure(2, weight=1)

win.mainloop()
