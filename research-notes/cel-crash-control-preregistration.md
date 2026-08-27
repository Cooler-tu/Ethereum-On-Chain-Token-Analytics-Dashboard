# CEL crash/control replication — pre-registration

Date frozen: 2026-08-27

This note freezes the first replication of the FTT same-token crash/control
design before any CEL outcome correlation is calculated.  The purpose is to
test whether the FTT result generalizes without choosing metrics or horizons in
response to CEL's answer.

## Event anchor and operational cutoff

The event is Celsius's public halt of customer withdrawals, transfers, and
swaps.  The [SEC complaint](https://www.sec.gov/file/comp-pr2023-133) states
that Celsius halted those operations on June 12, 2022.  A contemporaneous
report places the announcement at approximately 10:10 p.m. U.S. Eastern time,
or `2022-06-13 02:10 UTC`; see
[Blockworks](https://blockworks.com/news/celsius-lending-platform-suspends-withdrawals-and-transfers).

The operational cutoff is therefore frozen at `2022-06-13 02:10 UTC`.  Ethereum
block `14953505` has timestamp `02:09:50 UTC`, while block `14953506` is after
the cutoff.  The old feasibility table used block `14955880` (`12:00:14 UTC`),
about ten hours later; that approximation is replaced before formal indexing
so post-announcement trading is not mixed into the predictor window.

## Frozen windows

The windows are adjacent 30-day UTC intervals with no overlapping blocks.

| Window | UTC | Blocks (inclusive) | Role |
|---|---|---:|---|
| Control | 2022-04-14 02:10 → 2022-05-14 02:10 | `14580784–14770985` | Same token and pools before the crash window |
| Crash | 2022-05-14 02:10 → 2022-06-13 02:10 | `14770986–14953505` | Ends immediately before the public pause cutoff |

Block `14580783` is timestamped `02:09:24 UTC` and block `14580784` is the
first block after the control boundary (`02:10:26 UTC`).  Block `14770986` is
timestamped exactly `2022-05-14 02:10:00 UTC`.

## Frozen pool universe

The primary universe is fixed in `research-inputs/cel-primary-pools.json`:

| Pool | Version | Fee | CEL at control start | WETH at control start | Control early/late Swap sample | Crash early/late Swap sample |
|---|---|---:|---:|---:|---:|---:|
| `0xa5E7…9Fe6` | V2 | — | 136,445.9718 | 95.2665 | 208 / 749 | 423 / 850 |
| `0x0672…5105` | V3 | 0.30% | 1,542,087.4421 | 35.1100 | 239 / 197 | 193 / 162 |

Each sample covers 10,000 blocks at the beginning or end of its window.  These
counts are feasibility evidence only; no price return or predictor correlation
was inspected.  Both contracts existed at the control start and held non-zero
CEL and WETH at the control start, crash start, and cutoff.

The CEL/WETH V3 1% pool (`0xde2A…0c98`) is excluded because all four samples had
zero Swaps.  CEL/stablecoin pools are excluded to avoid mixing quote units.
Uniswap V1 is excluded from the primary replication so the protocol
architecture matches the FTT V2/V3 design.  These exclusions are frozen and
will not be revisited after outcomes are visible.

## Frozen variables, hypotheses, and inference

The FTT design is reused without changing directions:

| Predictor at hour t | Outcome | Frozen direction |
|---|---|---|
| `actual_transfer_net_ratio` | future 24h CEL/WETH log return | Negative |
| `net_lp_flow_ratio` | future 24h CEL/WETH log return | Positive |
| `gross_lp_activity_ratio` | future absolute 24h CEL/WETH log return | Positive |

- Base rows are hourly and aggregated across the two fixed pools.
- Ratios use the prior bucket's measured CEL reserve.
- Both price endpoints must have `price_trade_count > 0`; carried-only endpoints
  are excluded.
- Primary method: Spearman correlation, estimated separately in crash/control.
- Dependence: 24-paired-observation moving-block bootstrap, 1,999 repetitions.
- Crash null: 4,999 block permutations.
- Multiplicity: BH-FDR across the three primary crash tests, `q < 0.05`.
- Difference: independent moving-block-bootstrap CI for `crash − control`.
- Seed: `20260824`, unchanged from FTT.
- Confirmation still requires the frozen direction, a crash CI excluding zero,
  crash BH `q < 0.05`, and a crash-minus-control CI excluding zero.
- Future 48/72-hour returns, Pearson, and 6/12/24-hour buckets remain secondary
  and explicitly exploratory.

The same stop rules apply: at least 90% hourly reserve coverage, at least 90%
quantified Mint/Burn amounts, and at least 80 primary pairs per window.  Missing
amounts are never converted to zero.  Position Manager identity is skipped and
must remain unavailable rather than being interpreted as no LP activity.

## Frozen collection and validation commands

```bash
set -a
source .env
set +a
export ETH_LOG_CHUNK_SIZE=10000
export ETH_BLOCK_BATCH_SIZE=20

python3 -m src.cli analyze 0xaaAEBE6Fe48E54f431b0C390CfaF0b017d09D42d \
  --from-block 14580784 --to-block 14770985 \
  --pools-file research-inputs/cel-primary-pools.json \
  --index-source rpc --holdings-source rpc \
  --skip-position-manager --pool-transfers-only --artifact-format both \
  --output-dir output-cel-control-30d

python3 -m src.cli analyze 0xaaAEBE6Fe48E54f431b0C390CfaF0b017d09D42d \
  --from-block 14770986 --to-block 14953505 \
  --incident-block 14953505 \
  --pools-file research-inputs/cel-primary-pools.json \
  --index-source rpc --holdings-source rpc \
  --skip-position-manager --pool-transfers-only --artifact-format both \
  --output-dir output-cel-crash-30d

python3 scripts/crash_control_validation.py \
  --control-dir output-cel-control-30d \
  --crash-dir output-cel-crash-30d \
  --study-label CEL \
  --out-dir output-cel-crash-30d/research-crash-control
```

The correlation command is not run until both collections pass the frozen data
quality checks.
