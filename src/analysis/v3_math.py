"""Uniswap V3 math: convert position L + ticks + price → token amounts.

Uses the same relations as periphery ``LiquidityAmounts.getAmountsForLiquidity``.
Tick boundaries use Uniswap's integer Q128.128 algorithm. Decimal approximation
can create phantom balances for very large liquidity at extreme boundaries.
"""
from __future__ import annotations

from decimal import Decimal, getcontext

Q96 = 2**96
MIN_TICK = -887272
MAX_TICK = 887272

getcontext().prec = 80


def tick_to_sqrt_price_x96(tick: int) -> int:
    """sqrtPriceX96 = sqrt(1.0001**tick) * 2**96."""
    if tick < MIN_TICK or tick > MAX_TICK:
        raise ValueError("tick out of range: {}".format(tick))
    # Mathematical fixed-point factors and rounding from Uniswap TickMath:
    # https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/TickMath.sol
    factors = (
        0xfffcb933bd6fad37aa2d162d1a594001,
        0xfff97272373d413259a46990580e213a,
        0xfff2e50f5f656932ef12357cf3c7fdcc,
        0xffe5caca7e10e4e61c3624eaa0941cd0,
        0xffcb9843d60f6159c9db58835c926644,
        0xff973b41fa98c081472e6896dfb254c0,
        0xff2ea16466c96a3843ec78b326b52861,
        0xfe5dee046a99a2a811c461f1969c3053,
        0xfcbe86c7900a88aedcffc83b479aa3a4,
        0xf987a7253ac413176f2b074cf7815e54,
        0xf3392b0822b70005940c7a398e4b70f3,
        0xe7159475a2c29b7443b29c7fa6e889d9,
        0xd097f3bdfd2022b8845ad8f792aa5825,
        0xa9f746462d870fdf8a65dc1f90e061e5,
        0x70d869a156d2a1b890bb3df62baf32f7,
        0x31be135f97d08fd981231505542fcfa6,
        0x9aa508b5b7a84e1c677de54f3e99bc9,
        0x5d6af8dedb81196699c329225ee604,
        0x2216e584f5fa1ea926041bedfe98,
        0x48a170391f7dc42444e8fa2,
    )
    ratio = 1 << 128
    for bit, factor in enumerate(factors):
        if abs(int(tick)) & (1 << bit):
            ratio = ratio * factor >> 128
    if tick > 0:
        ratio = ((1 << 256) - 1) // ratio
    return (ratio + (1 << 32) - 1) >> 32


def get_amount0_for_liquidity(sqrt_a: int, sqrt_b: int, liquidity: int) -> int:
    if sqrt_a > sqrt_b:
        sqrt_a, sqrt_b = sqrt_b, sqrt_a
    if sqrt_a <= 0 or sqrt_b <= 0 or liquidity <= 0:
        return 0
    # L * (sqrt_b - sqrt_a) / (sqrt_a * sqrt_b) * 2^96
    return liquidity * (sqrt_b - sqrt_a) * Q96 // (sqrt_a * sqrt_b)


def get_amount1_for_liquidity(sqrt_a: int, sqrt_b: int, liquidity: int) -> int:
    if sqrt_a > sqrt_b:
        sqrt_a, sqrt_b = sqrt_b, sqrt_a
    if liquidity <= 0:
        return 0
    # L * (sqrt_b - sqrt_a) / 2^96
    return liquidity * (sqrt_b - sqrt_a) // Q96


def get_amounts_for_liquidity(
    sqrt_price_x96: int,
    tick_lower: int,
    tick_upper: int,
    liquidity: int,
) -> tuple[int, int]:
    """Return raw (amount0, amount1) for a position at the given pool price."""
    if liquidity <= 0 or tick_lower >= tick_upper:
        return 0, 0

    sqrt_a = tick_to_sqrt_price_x96(tick_lower)
    sqrt_b = tick_to_sqrt_price_x96(tick_upper)
    sqrt_p = int(sqrt_price_x96)

    if sqrt_p <= sqrt_a:
        return get_amount0_for_liquidity(sqrt_a, sqrt_b, liquidity), 0
    if sqrt_p < sqrt_b:
        return (
            get_amount0_for_liquidity(sqrt_p, sqrt_b, liquidity),
            get_amount1_for_liquidity(sqrt_a, sqrt_p, liquidity),
        )
    return 0, get_amount1_for_liquidity(sqrt_a, sqrt_b, liquidity)


def value_in_token1_raw(amount0: int, amount1: int, sqrt_price_x96: int) -> float:
    """Value both sides in raw token1 units (token1 per token0 from sqrtPrice)."""
    if sqrt_price_x96 <= 0:
        return float(amount1)
    price_1_per_0 = (float(sqrt_price_x96) / float(Q96)) ** 2
    return float(amount1) + float(amount0) * price_1_per_0
