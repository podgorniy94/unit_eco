from math import ceil

product = "printer"
price = "52"
dimension = (ceil(55.5), ceil(22.5), ceil(32))  # width, high, length
amount_in_box = 50
prod_amount = 3000
box_amount = ceil(prod_amount / amount_in_box)
box_weight = 21
total_weight = box_amount * box_weight
volume = dimension[0] * dimension[1] * dimension[2] / 1000000 * box_amount

total_weight = ceil(total_weight + (volume / 2 * 50))
volume = round(volume + (volume / 2 * 0.5), 2)
density = round(total_weight / volume, 2)

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

cargo_coef = (
    cargo_dict[max(filter(lambda x: x <= density, cargo_dict.keys()))] - discount
    if density >= 100
    else 600 * volume
)

print(cargo_coef)
print(total_weight, volume, density)
