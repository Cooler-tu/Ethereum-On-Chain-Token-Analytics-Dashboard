# Analysis Series Summary

## Dataset

| Field | Value |
|---|---:|
| Token | GALA `0xd1d2eb1b1e90b638588728b4130137d262c87cae` |
| All rows | 2163 |
| Pool rows | 1442 |
| Token-total buckets | 721 |
| Observed pools | 2 |
| Bucket seconds | 3600 |
| First bucket (UTC) | 2024-04-20T19:00:00+00:00 |
| Last bucket (UTC) | 2024-05-20T19:00:00+00:00 |
| TVL source | rpc_target_balance_local_price (721) |
| Price unit | WETH |
| Liquidity event coverage | collected |

## Coverage

| Check | Rows |
|---|---:|
| Pool rows with VWAP | 1287 |
| Pool rows with TVL state | 1442 |
| Max TVL-measured pools per bucket | 2 / 2 |
| Removal activity with unknown amount | 0 |
| Active LP rows with full identity coverage | 0 |

## Interpretation warnings

- RPC TVL is target-token-side attributable reserve, not full two-sided TVL.
- Price is quoted in WETH; returns are usable within this pool, but absolute values are not USD prices.
- No active pool×bucket has complete LP identity coverage; active_lp_count is not approved for correlation.

## Human-readable preview

`analysis_series_preview.csv` contains only `scope=token_total` rows. The full pool-level and token-total dataset remains in `tables/analysis_series.parquet`.
