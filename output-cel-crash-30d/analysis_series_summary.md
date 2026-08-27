# Analysis Series Summary

## Dataset

| Field | Value |
|---|---:|
| Token | CEL `0xaaaebe6fe48e54f431b0c390cfaf0b017d09d42d` |
| All rows | 2160 |
| Pool rows | 1439 |
| Token-total buckets | 721 |
| Observed pools | 2 |
| Bucket seconds | 3600 |
| First bucket (UTC) | 2022-05-14T02:00:00+00:00 |
| Last bucket (UTC) | 2022-06-13T02:00:00+00:00 |
| TVL source | rpc_target_balance_local_price (721) |
| Price unit | WETH |
| Liquidity event coverage | collected |

## Coverage

| Check | Rows |
|---|---:|
| Pool rows with VWAP | 1012 |
| Pool rows with TVL state | 1439 |
| Max TVL-measured pools per bucket | 2 / 2 |
| Removal activity with unknown amount | 0 |
| Active LP rows with full identity coverage | 0 |

## Interpretation warnings

- RPC TVL is target-token-side attributable reserve, not full two-sided TVL.
- Price is quoted in WETH; returns are usable within this pool, but absolute values are not USD prices.
- No active pool×bucket has complete LP identity coverage; active_lp_count is not approved for correlation.

## Human-readable preview

`analysis_series_preview.csv` contains only `scope=token_total` rows. The full pool-level and token-total dataset remains in `tables/analysis_series.parquet`.
