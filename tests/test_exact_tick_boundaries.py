from src.analysis.v3_math import tick_to_sqrt_price_x96, get_amounts_for_liquidity

def test_protocol_boundary_vectors():
    assert tick_to_sqrt_price_x96(-887272) == 4295128739
    assert tick_to_sqrt_price_x96(0) == 2**96
    assert tick_to_sqrt_price_x96(887272) == 1461446703485210103287273052203988822378723970342

def test_extreme_lower_boundary_has_no_phantom_token1():
    # uPEG V4 block 25680626: huge L amplifies a tiny boundary discrepancy.
    price = tick_to_sqrt_price_x96(733400)
    amount0, amount1 = get_amounts_for_liquidity(price,733400,733780,9021638751197675961507863187794205)
    assert amount0 > 0
    assert amount1 == 0

def test_observed_upeg_extreme_swap_price():
    # Actual preceding Swap at log 33 of block 25680626.
    _, amount1 = get_amounts_for_liquidity(666288027136667754139637815150162640183164947,733400,733780,9021638751197675961507863187794205)
    assert amount1 == 9880022320354507
