import json
import os
import sys
from math import ceil
from tkinter import filedialog, messagebox, simpledialog, ttk

import customtkinter as cttk
import openpyxl
import requests
from pyperclip import copy

cttk.set_appearance_mode("light")
cttk.set_default_color_theme("dark-blue")

win = cttk.CTk()
win.title("Calculation")
win.geometry("660x650")
win.grid_columnconfigure((0, 1, 2), weight=1)


# --- Main Logic
validated = 0


def add_data_to_excel():
    if validated:
        product_name = simpledialog.askstring("Товар", "Введите название товара:")
        if product_name:
            data = [product_name]
        else:
            return

        data = data + [entry.get() for entry in entries]
        data.append(currency.get())
        data = data + [button.cget("text")[:-2] for button in buttons]

        try:
            file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            if file:
                workbook = openpyxl.load_workbook(file)
                sheet = workbook.active
                last_column = sheet.max_column + 1

                for row_num, data_item in enumerate(data, start=1):
                    sheet.cell(row=row_num, column=last_column, value=data_item)
                workbook.save(file)
                workbook.close()
                messagebox.showinfo("Успех", "Данные успешно импортированы в Excel!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    else:
        messagebox.showerror("Ошибка", "Произведите рассчеты")


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


data = resource_path("data.json")


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


def dec_number(number):
    return f"{number:.0f}" if number.is_integer() else f"{number}"


def clean(field):
    value = field.get()
    if value == mandatory or value == not_digit or value == int_notif or value == "0":
        field.configure(text_color="black")
        field.delete(0, cttk.END)


def copy_to_clip(text):
    if text and text != " ":  # ctk button bug
        copy(text[:-2])


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


def read_cargo_data():

    with open(data, "r") as file:
        json_to_dict = json.load(file)
        cargo_dict = json_to_dict["coefficient"]
        discount = json_to_dict["discount"]
        return cargo_dict, discount


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
        global validated
        validated = 1
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
        log_price = cargo_coeff * total_weight * float(curr_var.get())
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

    for entry in entries:
        value = entry.get()

        if "," in value:
            upd_val = value.replace(",", ".")
            entry.delete(0, cttk.end)
            entry.insert(0, upd_val)

        if not value:
            entry.insert(0, mandatory)
            entry.configure(text_color="red")
            valid = 0
        elif value == mandatory or value == int_notif or value == not_digit:
            valid = 0
            continue
        elif value == not_digit:
            entry.delete(0, cttk.END)
            entry.insert(0, mandatory)
            valid = 0
        elif not all(digit in digits_seps for digit in value):
            entry.delete(0, cttk.END)
            entry.insert(0, not_digit)
            entry.configure(text_color="red")
            valid = 0
        elif value == "0":
            entry.delete(0, cttk.END)
            entry.insert(0, "0")
            entry.configure(text_color="red")
            valid = 0
    return valid


# --- Params
create_label("Цена в Китае", 0, 0)
price = create_entry()
place_entry(price, 1, 0)

create_label("Количество", 0, 1)
prod_amount = create_entry()
place_entry(prod_amount, 1, 1)

create_label("Кол. шт. в коробке", 0, 2)
amount_in_box = create_entry()
place_entry(amount_in_box, 1, 2)

create_label("Высота", 2, 0)
height = create_entry()
place_entry(height, 3, 0)

create_label("Ширина", 2, 1)
width = create_entry()
place_entry(width, 3, 1)

create_label("Длина", 2, 2)
length = create_entry()
place_entry(length, 3, 2)

create_label("Вес", 4, 0)
box_weight = create_entry()
place_entry(box_weight, 5, 0)


curr_var = cttk.StringVar(value="7.25")

get_curr()  # --- Getting latest USD/CNY currency
create_label("Курс $/¥ ", 4, 1)
currency = cttk.CTkEntry(win, textvariable=curr_var)
place_entry(currency, 5, 1)


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


entries = [price, prod_amount, amount_in_box, height, width, length, box_weight]
buttons = [goods_cost_bt, package_bt, insurance_bt, total_cost_bt, one_goods_bt, log_bt]

calculate_bt = cttk.CTkButton(
    win,
    text="Рассчитать",
    command=calculate,
    hover_color="#389147",
    text_color="white",
    fg_color="#3fa24f",
).grid(row=5, column=2, padx=(25, 0), sticky="we")

# --- Creating cargo table


def create_table():
    no_den_var = cttk.IntVar(value="")
    coeff_var = cttk.StringVar(value=None)
    den_var = cttk.StringVar(value=None)
    dis_var = cttk.StringVar(value=None)
    global discount
    cargo_dict, discount = read_cargo_data()

    def select_item(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            # Filling fields below table based on the selected one.
            record = item["values"]  # return int I/O str if it's not float
            no_den_var.set(f"{record[0]} / {record[1]}")
            den_var.set(record[1])
            coeff_var.set(str(record[2]))
            dis_var.set(dec_number(discount))

            # Focusing on the field with the coefficient
            coeff_entry.focus_set()
            coeff_entry.icursor(len(str(record[2])))

    def deselect_item():
        selected_item = tree.selection()
        if selected_item:
            tree.selection_remove(selected_item)
            no_den_var.set(""), coeff_var.set(""), dis_var.set("")
            win.focus_set()

    def create_label(text, row, column):
        cttk.CTkLabel(win, text=text, anchor="w").grid(
            row=row, column=column, sticky="we", padx=(25, 0)
        )

    def load_table(cargo_dict):
        for i, k in enumerate(cargo_dict):
            tree.insert("", i, text=i + 1, values=(i + 1, k, cargo_dict[k]))

    def save_cargo():
        if tree.selection():
            coeff_val = coeff_entry.get()
            global discount
            discount = float(dis_entry.get())

            if "," in coeff_val:
                upd_val = coeff_val.replace(",", ".")
                coeff_entry.delete(0, cttk.END)
                coeff_entry.insert(0, upd_val)
                coeff_val = upd_val
            coeff_val = float(coeff_val)

            number = dec_number(coeff_val)
            cargo_dict[den_var.get()] = str(number)

            with open(data, "w") as file:
                dict_to_json = {"coefficient": cargo_dict, "discount": discount}
                json.dump(dict_to_json, file)

            tree.delete(*tree.get_children())
            load_table(cargo_dict)
            no_den_var.set(""), coeff_var.set(""), dis_var.set("")
            win.focus_set()

    # Tree creating
    tree = ttk.Treeview(win, columns=("No", "Density", "Coeff"), show="headings")
    ttk.Style().theme_use("default")

    tree.grid(
        row=10, column=0, columnspan=3, sticky="nsew", padx=(20, 0), pady=(20, 10)
    )
    tree.column("No", minwidth=25)
    tree.column("Density", minwidth=25)
    tree.column("Coeff", minwidth=25)

    tree.heading("No", text="No", anchor=cttk.CENTER)
    tree.heading("Density", text="Плотность", anchor=cttk.W)
    tree.heading("Coeff", text="Коэффициент", anchor=cttk.W)

    scrollbar = cttk.CTkScrollbar(win, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=10, column=3, sticky="nsw", pady=(20, 10), padx=(0, 10))

    # Populated table with values
    load_table(cargo_dict)

    # Fields under table
    create_label("No / Плотность", 11, 0)
    create_label("Коэффициент", 11, 1)
    create_label("Скидка", 11, 2)

    no_den_lb = cttk.CTkLabel(win, textvariable=no_den_var, fg_color="light gray")
    no_den_lb.grid(row=12, column=0, sticky="we", padx=(25, 0))

    coeff_entry = cttk.CTkEntry(win, textvariable=coeff_var)
    coeff_entry.grid(row=12, column=1, sticky="we", padx=(25, 0))

    dis_entry = cttk.CTkEntry(win, textvariable=dis_var)
    dis_entry.grid(row=12, column=2, sticky="we", padx=(25, 0))

    tree.bind("<<TreeviewSelect>>", select_item)

    cttk.CTkButton(win, text="Отменить", command=deselect_item).grid(
        row=15, column=0, padx=(25, 0), pady=15, sticky="we"
    )
    cttk.CTkButton(win, text="Сохранить", command=save_cargo).grid(
        row=15, column=2, padx=(25, 0), pady=15, sticky="we"
    )

    return cargo_dict, discount


# --- Excel export
cttk.CTkButton(win, text="Импортировать в Excel", command=add_data_to_excel).grid(
    row=15, column=1, padx=(25, 0), pady=15, sticky="we"
)


create_table()


win.mainloop()
