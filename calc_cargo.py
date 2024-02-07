import json
import tkinter as tk
from tkinter import ttk


def read_cargo_data(file):
    with open(file, "r") as file:
        return json.load(file)


def create_table(win):
    no_den_var = tk.IntVar(value="")
    coeff_var = tk.StringVar(value=None)
    den_var = tk.StringVar(value=None)
    dis_var = tk.StringVar(value=None)

    json_to_dict = read_cargo_data("cargo_data.json")
    cargo_dict = json_to_dict["coefficient"]
    global discount
    discount = json_to_dict["discount"]

    def select_item(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            # Filling fields below table based on the selected one.
            record = item["values"]  # return int I/O str if it's not float
            no_den_var.set(f"{record[0]} / {record[1]}")
            den_var.set(record[1])
            coeff_var.set(str(record[2]))
            dis_var.set(discount)

            # Focusing on the field with the coefficient
            coeff_entry.focus_set()
            coeff_entry.icursor(len(str(record[2])))

    def deselect_item():
        selected_item = tree.selection()
        if selected_item:
            tree.selection_remove(selected_item)
            no_den_var.set(""), coeff_var.set(""), dis_var.set("")
            win.focus_set()

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
                coeff_entry.delete(0, tk.END)
                coeff_entry.insert(0, upd_val)
                coeff_val = upd_val
            coeff_val = float(coeff_val)

            number = f"{coeff_val:.0f}" if coeff_val.is_integer() else f"{coeff_val}"
            cargo_dict[den_var.get()] = str(number)

            with open("cargo_data.json", "w") as file:
                dict_to_json = {"coefficient": cargo_dict, "discount": discount}
                json.dump(dict_to_json, file)

            tree.delete(*tree.get_children())
            load_table(cargo_dict)
            no_den_var.set(""), coeff_var.set(""), dis_var.set("")
            win.focus_set()

    # Tree creating
    tree = ttk.Treeview(win, columns=("No", "Density", "Coeff"), show="headings")

    tree.grid(row=10, column=0, columnspan=3, sticky="nsew", padx=5, pady=20)
    tree.column("No", minwidth=25)
    tree.column("Density", minwidth=25)
    tree.column("Coeff", minwidth=25)

    tree.heading("No", text="No", anchor=tk.CENTER)
    tree.heading("Density", text="Плотность", anchor=tk.W)
    tree.heading("Coeff", text="Коэффициент", anchor=tk.W)

    scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=10, column=3, sticky="nsw", pady=20, padx=5)

    # Populated table with values
    load_table(cargo_dict)

    # Fields under table
    tk.Label(win, text="No / Плотность").grid(row=11, column=0, sticky="w", padx=3)
    tk.Label(win, text="Коэффициент").grid(row=11, column=1, sticky="w", padx=3)
    tk.Label(win, text="Скидка").grid(row=11, column=2, sticky="w", padx=3)

    no_den_lb = tk.Label(win, borderwidth=1, relief="ridge", textvariable=no_den_var)
    no_den_lb.grid(row=12, column=0, sticky="we", padx=5)

    coeff_entry = tk.Entry(win, textvariable=coeff_var)
    coeff_entry.grid(row=12, column=1, sticky="we", padx=5)

    dis_entry = tk.Entry(win, textvariable=dis_var)
    dis_entry.grid(row=12, column=2, sticky="we", padx=5)

    tree.bind("<<TreeviewSelect>>", select_item)

    tk.Button(win, text="Отменить", command=deselect_item).grid(
        row=15, column=0, padx=3, pady=10, sticky="we"
    )
    tk.Button(win, text="Сохранить", command=save_cargo).grid(
        row=15, column=2, padx=3, pady=10, sticky="we"
    )
