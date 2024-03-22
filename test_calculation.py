from contextlib import nullcontext

import pytest

from calculation import Calculation


class TestCalculation:
    @pytest.mark.parametrize(
        "product_amount, amount_in_box, box_weight, height, width, length, density_result, expect",
        [
            (3000, 50, 21, 55.5, 22.5, 32, 441, nullcontext()),
            (3000, 50, 24, 50, 28, 34, 424, nullcontext()),
            (3000, 50, 13, 29, 31, 63, 204, nullcontext()),
            (3000, 60, 15, 62, 26, 64, 137, nullcontext()),
            (3000, "60", 15, 62, 26, 64, 137, pytest.raises(TypeError)),
            (3000, 0, 15, 62, 26, 64, 137, pytest.raises(ZeroDivisionError)),
        ],
    )
    def test_calculate_density(
        self,
        product_amount,
        amount_in_box,
        box_weight,
        height,
        width,
        length,
        density_result,
        expect,
    ):
        density = Calculation.calculate_density
        args = product_amount, amount_in_box, box_weight, height, width, length

        with expect:
            assert density(*args) == density_result
