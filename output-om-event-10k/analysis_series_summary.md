# Analysis Series Summary

## Dataset

| Field | Value |
|---|---:|
| Token | OM `0x3593d125a4f7849a1b059e64f4517a86dd60c95d` |
| All rows | 101 |
| Pool rows | 67 |
| Token-total buckets | 34 |
| Observed pools | 3 |
| Bucket seconds | 3600 |
| First bucket (UTC) | 2025-04-12T09:00:00+00:00 |
| Last bucket (UTC) | 2025-04-13T18:00:00+00:00 |
| TVL source | rpc_target_balance_local_price (34) |
| Price unit | WETH |
| Liquidity event coverage | collected |

## Coverage

| Check | Rows |
|---|---:|
| Pool rows with VWAP | 54 |
| Pool rows with TVL state | 67 |
| Max TVL-measured pools per bucket | 3 / 7 |
| Removal activity with unknown amount | 0 |
| Active LP rows with full identity coverage | 2 |

## Interpretation warnings

- RPC TVL is target-token-side attributable reserve, not full two-sided TVL.
- Token-total TVL covers at most 3 of 7 verified pools; market-wide volume/price versus this partial TVL is not approved as a formal market-wide finding.
- Price is quoted in WETH; returns are usable within this pool, but absolute values are not USD prices.

## Human-readable preview

`analysis_series_preview.csv` contains only `scope=token_total` rows. The full pool-level and token-total dataset remains in `tables/analysis_series.parquet`.
