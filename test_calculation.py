from contextlib import nullcontext

import pytest

from calculation import Calculation


class TestCalculation:
    @pytest.mark.parametrize(
        "product_amount, amount_in_box, box_weight, height, width, length, density_result, expect",
        [
            (3000, 50, 21, 55.5, 22.5, 32, (441, 1319.94, 3.0), nullcontext()),
            (3000, 50, 24, 50, 28, 34, (424, 1511.4, 3.57), nullcontext()),
            (3000, 50, 13, 29, 31, 63, (204, 864.96, 4.25), nullcontext()),
            (3000, 60, 15, 62, 26, 64, (137, 878.96, 6.45), nullcontext()),
            (3000, "60", 15, 62, 26, 64, (137, 878.96, 6.45), pytest.raises(TypeError)),
            (3000, 0, 15, 62, 26, 64, (), pytest.raises(ZeroDivisionError)),
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

    @pytest.mark.parametrize(
        "density, total_weight, total_volume, currency, cargo",
        [
            (441, 1319.94, 3.0, 7.2, 18057),
            (424, 1511.4, 3.57, 7.2, 20676),
            (204, 864.96, 4.25, 7.2, 14324),
            (137, 878.96, 6.45, 7.2, 18986),
        ],
    )
    def test_calculate_cargo(
        self, density, total_weight, total_volume, currency, cargo
    ):
        args = density, total_weight, total_volume, currency
        assert Calculation.calculate_cargo(*args) == cargo

    @pytest.mark.parametrize(
        "price, product_amount, total_volume, cargo, costs",
        [
            (52, 3000, 3.0, 18057, (156000, 630, 1560, 176247, 58.75, 18057)),
            (89, 3000, 3.57, 20676, (267000, 749.7, 2670, 291095.7, 97.03, 20676)),
            (37, 3000, 4.25, 14324, (111000, 892.5, 1110.0, 127326.5, 42.44, 14324)),
            (62, 3000, 6.45, 18986, (186000, 1354.5, 1860.0, 208200.5, 69.4, 18986)),
        ],
    )
    def test_calculate_cost(self, price, product_amount, total_volume, cargo, costs):
        args = price, product_amount, total_volume, cargo
        assert Calculation.calculate_costs(*args) == costs
