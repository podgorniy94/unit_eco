import pytest

from calculation import Calculation


class TestCalculation:
    @pytest.mark.parametrize(
        "product_amount, amount_in_box, box_weight, height, width, length, density_result",
        [
            (3000, 50, 21, 55.5, 22.5, 32, 441),
            (3000, 50, 24, 50, 28, 34, 424),
            (3000, 50, 13, 29, 31, 63, 204),
            (3000, 60, 15, 62, 26, 64, 137),
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
    ):
        density = Calculation.calculate_density
        assert (
            density(product_amount, amount_in_box, box_weight, height, width, length)
            == density_result
        )
