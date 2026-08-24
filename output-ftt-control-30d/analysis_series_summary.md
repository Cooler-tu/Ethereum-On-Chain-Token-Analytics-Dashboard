# Analysis Series Summary

## Dataset

| Field | Value |
|---|---:|
| Token | FTX Token `0x50d1c9771902476076ecfc8b2a83ad6b9355a4c9` |
| All rows | 2858 |
| Pool rows | 2142 |
| Token-total buckets | 716 |
| Observed pools | 3 |
| Bucket seconds | 3600 |
| First bucket (UTC) | 2022-09-09T20:00:00+00:00 |
| Last bucket (UTC) | 2022-10-09T15:00:00+00:00 |
| TVL source | rpc_target_balance_local_price (716) |
| Price unit | WETH |
| Liquidity event coverage | collected |

## Coverage

| Check | Rows |
|---|---:|
| Pool rows with VWAP | 500 |
| Pool rows with TVL state | 2142 |
| Max TVL-measured pools per bucket | 3 / 3 |
| Removal activity with unknown amount | 0 |
| Active LP rows with full identity coverage | 0 |

## Interpretation warnings

- RPC TVL is target-token-side attributable reserve, not full two-sided TVL.
- Price is quoted in WETH; returns are usable within this pool, but absolute values are not USD prices.
- No active pool×bucket has complete LP identity coverage; active_lp_count is not approved for correlation.

## Human-readable preview

`analysis_series_preview.csv` contains only `scope=token_total` rows. The full pool-level and token-total dataset remains in `tables/analysis_series.parquet`.
