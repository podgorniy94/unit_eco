import json
from tkinter import ttk


def dec_number(number):
    return f"{number:.0f}" if number.is_integer() else f"{number}"


def read_cargo_data():
    with open("cargo_data.json", "r") as file:
        json_to_dict = json.load(file)
        cargo_dict = json_to_dict["coefficient"]
        discount = json_to_dict["discount"]
        return cargo_dict, discount


def create_table(win, cttk):
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

            with open("cargo_data.json", "w") as file:
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
        row=15, column=0, padx=(25, 0), pady=10, sticky="we"
    )
    cttk.CTkButton(win, text="Сохранить", command=save_cargo).grid(
        row=15, column=2, padx=(25, 0), pady=10, sticky="we"
    )

    return cargo_dict, discount
