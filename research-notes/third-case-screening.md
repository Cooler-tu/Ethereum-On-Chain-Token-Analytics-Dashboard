# Third-case inventory-mechanism screening

Date: 2026-08-29

This screen selects one final prospective case for the target-inventory
mechanism suggested by FTT and CEL. It uses public incident boundaries,
historical pool existence/reserves, and short Swap/Mint/Burn feasibility
samples only. No candidate's target-inventory feature, future-return
correlation, or event/control test was calculated.

## Candidates

| Candidate | Event boundary | Independence and interpretation | Pre-event WETH-pool feasibility | Decision |
|---|---|---|---|---|
| GALA | Unauthorized 5B GALA mint, `2024-05-20 19:32:11 UTC`, block `19913232` | Exact Ethereum transaction; attacker subsequently sold through Uniswap, independent of FTX/Celsius | Main V3 0.30% has 245/218 Swaps in pre-event early/late 10k-block samples; V2 has 93/52 | **Select** |
| EUL | Euler exploit, `2023-03-13 08:50:59 UTC`, block `16817996` | Exact protocol exploit and reported >45% EUL decline | V3 1% has 28/75 Swaps in the immediately preceding 30-day early/late samples; V2 has 0/2 | Feasible but materially thinner |
| CRV | CRV/ETH pool exploit, `2023-07-30 19:08:23 UTC`, block `17807830` | Exact event, but the shock directly drained the Curve CRV/ETH pool while the proposed study measures Uniswap | Main V3 0.30% has 111/122 pre-event early/late Swaps | Reject for mechanism mismatch |
| OM | 2025 CEX liquidation cascade | Exact approximate market time but primarily CEX-driven and token representation raises bridge/mirror sensitivity | Previously screened | Retain only as sensitivity case |
| CREDI | 2025 decline from ATH | No defensible single incident transaction or operational boundary | Previously screened | Reject |

Sources:

- Gala's official incident report states that a compromised minter role created
  five billion tokens: [Gala Games incident report](https://news.gala.com/gala-games/incident-report-unauthorized-token-minting-blockchain-game-partners-inc/).
- The exact unauthorized mint is Ethereum transaction
  [`0xa6d90a…77fe`](https://etherscan.io/tx/0xa6d90abe17d17743a9cecab84bcefb0fd0bbfa0c61bba60fd2f680b0a2f077fe),
  block `19913232`.
- Euler's foundation confirms the March 13 exploit:
  [Euler Governance Forum](https://forum.euler.finance/t/special-announcement/900).
- The CRV/ETH exploit began at 19:08 UTC and directly drained the Curve pool:
  [LlamaRisk postmortem](https://www.llamarisk.com/research/curve-pool-reentrancy-exploit-postmortem).

## GALA feasibility evidence

The selected token is GALA v2
`0xd1d2Eb1B1e90B638588728b4130137D262C87cae` (8 decimals). Exact adjacent
30-day windows are used because the mint transaction is the start of the shock,
not a public cutoff after a long deterioration.

| Pool | Version | GALA control start / incident−1 / event end | Control early/late Swaps | Event early/late Swaps | Event early/late Mint/Burn |
|---|---|---:|---:|---:|---:|
| `0x72B1…579A` | V2 | 616,956.52 / 654,763.81 / 947,360.05 | 93 / 52 | 409 / 59 | 0/0 / 0/0 |
| `0x465E…3719` | V3 0.30% | 114.096M / 42.137M / 37.223M | 245 / 218 | 1,730 / 143 | 61/59 / 2/3 |

Each early/late sample contains 10,000 blocks. Both selected contracts existed
at the control start and had non-zero GALA at all three boundaries. The V3 1%
pool (`0xF1Dd…1597`) is excluded before outcomes: its pre-event samples have
only 4/11 Swaps and its target reserve is below 0.35% of the main V3 pool.

GALA therefore passes the light screen without a full scan. The exact frozen
design is in `research-notes/gala-inventory-mechanism-preregistration.md`.
