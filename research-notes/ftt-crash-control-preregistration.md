# FTT crash/control validation — screening and pre-registration

Date frozen: 2026-08-24

This note was written before the full FTT event index or correlation result was
collected.  Its purpose is to prevent changing the case, pools, metrics, or lag
horizons after seeing the answer.

## Decision

Use **FTT** as the first independent crash case and the immediately preceding
30-day FTT window as the same-token control.  Keep **CEL** as the second
replication case.  Do not use OM or CREDI in the first validation.

The public event anchor is 2022-11-08, when the FTX liquidity crisis and
withdrawal halt became observable.  The operational cutoff is frozen at
`2022-11-08 16:00 UTC`, block `15926371`; it is an analysis boundary, not a
claim that the whole event happened in one block.  Supporting chronology:

- [U.S. House Financial Services Committee hearing record](https://democrats-financialservices.house.gov/uploadedfiles/hhrg-117-ba00-20221213-sd002.pdf)
- [21Shares FTX FAQ](https://cdn.21shares.com/uploads/current-documents/21Shares%20FTX%20FAQ.pdf)

## Low-cost feasibility screen

The screen used token metadata, Uniswap V1–V3 factory probes, historical
`balanceOf`, contract bytecode, and two 10,000-block Swap-count samples.  It did
not index full-window Transfers, Position Manager events, wallets, or outcomes.
The two samples are the first and last approximately 33 hours of each candidate's
pre-incident block window, so they are activity checks rather than formal tests.

| Candidate | Verified pools | Early Swap sample | Late Swap sample | Decision |
|---|---:|---:|---:|---|
| OM | 7 | 412 | 789 | Defer: active, but Ethereum/mirror and cross-chain structure add interpretation risk |
| FTT | 9 | 25 | 2,115 | Select: clear external event and a large DEX activity regime change |
| CEL | 11 | 182 | 1,487 | Reserve as the second replication case |
| CREDI | 2 | 62 | 149 | Exclude for now: no sufficiently clear, independently verified incident boundary |

For the three selected FTT/WETH pools alone, the last 10,000 blocks before the
incident contained `216 + 1,514 + 374 = 2,104` Swaps.  The last 10,000 blocks of
the control window contained only `1 + 1 + 5 = 7`.  All three pool contracts
already existed at the control start and held non-zero FTT and WETH there.

The Dune SQL path was not used because the configured `/api/v1/sql/execute`
endpoint returned `Deprecated query engine`.  This is a data-path failure, not
evidence of no market activity.  Formal indexing is therefore frozen to RPC.

## Frozen windows

UTC duration, rather than a fixed `216000`-block approximation, defines each
window.  This avoids the pre-/post-Merge block-time change making equal block
counts represent unequal clock time.

| Window | UTC | Blocks (inclusive) | Role |
|---|---|---:|---|
| Control | 2022-09-09 16:00 → 2022-10-09 16:00 | `15503619–15711589` | Same token and venues, before the crisis window |
| Crash | 2022-10-09 16:00 → 2022-11-08 16:00 | `15711590–15926371` | Ends at the frozen incident cutoff |

The primary pool universe is fixed in
`research-inputs/ftt-primary-pools.json`: one Uniswap V2 FTT/WETH pool and two
Uniswap V3 FTT/WETH pools (0.30% and 1.00%).  WETH-only quotation avoids mixing
stablecoin and WETH price units.  Position Manager identity will be skipped;
pool-level Swap/Mint/Burn and target-token Transfer evidence remains required.
Because the Transfer set is intentionally pool-scoped, the post-index holder
leaderboard refresh is skipped rather than presenting counterparties as a
complete holder sample.

## Frozen variables and hypotheses

Base rows are hourly and aggregated across the three fixed pools.  All ratios
use the previous bucket's measured FTT reserve as denominator.
Primary return pairs require an observed trade price (`price_trade_count > 0`)
at both the predictor-hour endpoint and the future-return endpoint; a
carried-forward-only endpoint is excluded rather than treated as a zero return.

| Variable | Definition | Role |
|---|---|---|
| `price_return` | log change in WETH per FTT close price | Outcome |
| `actual_transfer_net_ratio` | (FTT Transfer into pools − out of pools) / prior FTT reserve | Primary predictor; includes trading and liquidity movement |
| `net_lp_flow_ratio` | (FTT added − FTT removed from Mint/Burn evidence) / prior reserve | Primary predictor |
| `gross_lp_activity_ratio` | (FTT added + FTT removed) / prior reserve | Primary activity predictor |
| `recycling_share` | `2 × min(added, removed) / (added + removed)`; missing when no LP activity | Interpretation: high values indicate two-way repositioning |
| `volume_turnover` | FTT Swap volume / prior reserve | Context/control variable |

Primary tests use Spearman correlation between each of the first three
predictors and **future 24-hour price return**.  The crash and control windows
are estimated separately, followed by a moving-block-bootstrap difference
(`crash − control`).  A result is confirmatory only if:

1. the crash-window association has the pre-specified direction and its 95%
   moving-block-bootstrap interval excludes zero;
2. its block-permutation p-value survives BH-FDR across the three primary
   predictor tests (`q < 0.05`); and
3. the bootstrap interval for the crash-minus-control association excludes zero.

Direction is frozen as follows: more net FTT transferred into pools is expected
to precede a lower FTT price (negative); more net LP inflow is expected to
precede a higher price (positive); greater gross LP activity is expected to
precede a larger absolute return, so this test uses future absolute price return
(positive).

The dependence block is fixed at **24 paired observations** for both the
moving-block bootstrap and block-permutation test.  Primary intervals use 1,999
bootstrap repetitions; crash-window null tests use 4,999 block permutations.
All pseudo-random draws use seed `20260824`.  These choices were frozen after
coverage counts were known but before any outcome correlation was calculated.

Secondary, explicitly exploratory checks are future 48- and 72-hour returns,
Pearson correlation, and 6-/12-/24-hour bucket sensitivity.  Lag zero is a
mechanical diagnostic only.  No unregistered lag may be promoted to a finding.

## Data-quality stop rules

- Do not treat a missing amount as zero.
- Do not interpret V3 Position Manager identity as observed when it is skipped.
- Require historical reserve snapshots for at least 90% of included hourly rows.
- Require quantified LP amounts for at least 90% of included LP events; otherwise
  downgrade LP-flow tests to exploratory.
- If fewer than 80 paired observations remain for a primary test, report it as
  underpowered rather than widening the lag search.
- Report the DEX scope explicitly: FTX was principally a centralized-exchange
  crisis, and Ethereum Uniswap evidence cannot reconstruct the complete cause.

## Frozen collection commands

```bash
set -a
source .env
set +a
# Tenderly accepts 10,000-block eth_getLogs ranges. Omit this override for
# providers with smaller limits; the project default remains 2,000.
export ETH_LOG_CHUNK_SIZE=10000
# Tenderly's large block-header batches are slower than smaller responses on
# this historical window; 20 was fixed from a timing-only benchmark.
export ETH_BLOCK_BATCH_SIZE=20

python3 -m src.cli analyze 0x50D1C9771902476076eCFc8B2A83Ad6b9355a4c9 \
  --from-block 15503619 --to-block 15711589 \
  --pools-file research-inputs/ftt-primary-pools.json \
  --index-source rpc --holdings-source rpc \
  --skip-position-manager --pool-transfers-only --artifact-format both \
  --output-dir output-ftt-control-30d

python3 -m src.cli analyze 0x50D1C9771902476076eCFc8B2A83Ad6b9355a4c9 \
  --from-block 15711590 --to-block 15926371 \
  --incident-block 15926371 \
  --pools-file research-inputs/ftt-primary-pools.json \
  --index-source rpc --holdings-source rpc \
  --skip-position-manager --pool-transfers-only --artifact-format both \
  --output-dir output-ftt-crash-30d
```

The correlation comparison starts only after both collections pass the frozen
coverage checks.

```bash
python3 scripts/crash_control_validation.py \
  --control-dir output-ftt-control-30d \
  --crash-dir output-ftt-crash-30d \
  --out-dir output-ftt-crash-30d/research-crash-control
```
