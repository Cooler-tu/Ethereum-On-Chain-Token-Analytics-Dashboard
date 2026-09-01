# Analysis Series Summary

## Dataset

| Field | Value |
|---|---:|
| Token | CRV `0xd533a949740bb3306d119cc777fa900ba034cd52` |
| All rows | 34 |
| Pool rows | 17 |
| Token-total buckets | 17 |
| Observed pools | 1 |
| Bucket seconds | 3600 |
| First bucket (UTC) | 2026-08-31T14:00:00+00:00 |
| Last bucket (UTC) | 2026-09-01T06:00:00+00:00 |
| TVL source | rpc_target_balance_local_price (17) |
| Price unit | WETH |
| Liquidity event coverage | collected |

## Coverage

| Check | Rows |
|---|---:|
| Pool rows with VWAP | 17 |
| Pool rows with TVL state | 17 |
| Max TVL-measured pools per bucket | 1 / 1 |
| Removal activity with unknown amount | 0 |
| Active LP rows with full identity coverage | 1 |

## Interpretation warnings

- RPC TVL is target-token-side attributable reserve, not full two-sided TVL.
- Price is quoted in WETH; returns are usable within this pool, but absolute values are not USD prices.

## Human-readable preview

`analysis_series_preview.csv` contains only `scope=token_total` rows. The full pool-level and token-total dataset remains in `tables/analysis_series.parquet`.
