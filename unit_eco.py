import tkinter as tk
from math import ceil

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


def int_r(num):
    num = int(float(num) + 0.5)
    return num


def calculate():
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

    calculate_log(density, total_volume, total_weight)


def calculate_log(density, total_volume, total_weight):
    log = (
        (cargo_dict[max(filter(lambda x: x <= density, cargo_dict.keys()))] - discount)
        * total_weight
        * 7.25
        if density >= 100
        else 600 * total_volume
    )
    ddp_l["text"] = f"{round(log, 2)} ¥"


win = tk.Tk()
# photo = tk.PhotoImage(file=".png")
# win.iconphoto(False, photo)
win.title("Unit Economics")
win.geometry("500x600")

tk.Label(win, text="Товар").grid(row=0, column=0, sticky="w")
product = tk.Entry(win)
product.grid(row=1, column=0)

tk.Label(win, text="Цена").grid(row=0, column=1, sticky="w")
price = tk.Entry(win)
price.grid(row=1, column=1)

tk.Label(win, text="Количество").grid(row=0, column=2, sticky="w")
prod_amount = tk.Entry(win)
prod_amount.grid(row=1, column=2)

tk.Label(win, text="Высота").grid(row=2, column=0, sticky="w")
height = tk.Entry(win)
height.grid(row=3, column=0)

tk.Label(win, text="Ширина").grid(row=2, column=1, sticky="w")
width = tk.Entry(win)
width.grid(row=3, column=1)

tk.Label(win, text="Длина").grid(row=2, column=2, sticky="w")
length = tk.Entry(win)
length.grid(row=3, column=2)

tk.Label(win, text="Кол. шт. в коробке").grid(row=4, column=0, sticky="w")
amount_in_box = tk.Entry(win)
amount_in_box.grid(row=5, column=0)

tk.Label(win, text="Вес").grid(row=4, column=1, sticky="w")
box_weight = tk.Entry(win)
box_weight.grid(row=5, column=1)

tk.Button(
    win,
    text="Рассчитать",
    command=calculate,
).grid(row=4, column=2)

ddp_l = tk.Label(win, text="Конечная цена")
ddp_l.grid(row=5, column=2)

win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)
win.grid_columnconfigure(2, weight=1)


win.mainloop()
