# On-Chain Token Crash & Liquidity Risk Report

## Executive Summary

- **Token:** FTX Token ([0x50D1c977...55a4c9](https://etherscan.io/address/0x50D1c9771902476076eCFc8B2A83Ad6b9355a4c9))
- **Chain:** Ethereum (Chain ID: 1)
- **Analysis Window:** Block 15504720 to 15711337
- **Incident Block:** Not specified
- **Report Generated:** 2026-08-24 09:43:10 UTC

### Risk Score

| Metric | Value |
|--------|-------|
| **Final Risk Score** | **0.5017 / 1.00** |
| **Risk Level** | **MEDIUM** |
| Evidence Confidence | 91.00% |
| Visual | `██████████░░░░░░░░░░` |


## Token Profile

| Property | Value |
|----------|-------|
| Address | [0x50D1c977...55a4c9](https://etherscan.io/address/0x50D1c9771902476076eCFc8B2A83Ad6b9355a4c9) |
| Symbol | FTX Token |
| Name | FTT |
| Decimals | 18 (onchain) |
| Total Supply | 328895103.8132 |
| Is Contract | True |
| Proxy Address | None |
| Implementation | None |
| Behavior Flags | None |


## Pool Summary

**3** verified pool(s), **0** unverified candidate(s).

| Pool Address | Protocol | Version | Token0 | Token1 | Fee | Confidence |
|-------------|----------|---------|--------|--------|-----|------------|
| [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | uniswap | v2 | 0x50D1c977... | 0xC02aaA39... | N/A | 100.00% |
| [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | uniswap | v3 | 0x50D1c977... | 0xC02aaA39... | 3000 | 100.00% |
| [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | uniswap | v3 | 0x50D1c977... | 0xC02aaA39... | 10000 | 100.00% |


## Related Addresses

| Address | Label | Category | Confidence |
|---------|-------|----------|------------|
| [0x5C69bEe7...c5aA6f](https://etherscan.io/address/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f) | Factory (uniswap)_v2 | protocol_deployment | 100% |
| [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | Uniswap V2 Pool | pool | 100% |
| [0x7a250d56...F2488D](https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D) | Router (uniswap_v2) | router | 100% |
| [0x1F98431c...31F984](https://etherscan.io/address/0x1F98431c8aD98523631AE4a59f267346ea31F984) | Factory (uniswap)_v3 | protocol_deployment | 100% |
| [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Uniswap V3 Pool | pool | 100% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | PositionManager (uniswap_v3) | position_manager | 100% |
| [0xE592427A...861564](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564) | Router (uniswap_v3) | router | 100% |
| [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | Uniswap V3 Pool | pool | 100% |
| [0x772589e9...D9CF47](https://etherscan.io/address/0x772589e99bC9C54DD40acb7d73F88Ccbc9D9CF47) | Deployer | token_creator | 100% |
| [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x56178a0d...345Bf9](https://etherscan.io/address/0x56178a0d5F301bAf6CF3e1Cd53d9863437345Bf9) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x98C3d318...8d6B8E](https://etherscan.io/address/0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x7825dE55...3E1bf3](https://etherscan.io/address/0x7825dE5586E4d2FD04459091bbe783fa243E1bf3) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...43097d](https://etherscan.io/address/0x1111111254fb6c44bAC0beD2854e76F90643097d) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xF2F400C1...B1b8a8](https://etherscan.io/address/0xF2F400C138F9fb900576263af0BC7fCde2B1b8a8) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xD7c09E00...90A98A](https://etherscan.io/address/0xD7c09E006A2891880331b0F6224071C1e890A98A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x8c7918f8...665411](https://etherscan.io/address/0x8c7918f838452319962424A03C13D1510a665411) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x598a2659...986f8f](https://etherscan.io/address/0x598a265984e6e9ecD0955aF29675CC1C04986f8f) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x114419ab...9aa2Df](https://etherscan.io/address/0x114419abc1013475C0C8509fB4707b867B9aa2Df) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x98d5Bd6f...Ce1E6f](https://etherscan.io/address/0x98d5Bd6f3932b1cc4f979F93979308e6e9Ce1E6f) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x061d801C...41C175](https://etherscan.io/address/0x061d801C1Aeec7b1B5De17C76fBd8329BC41C175) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x5231E31C...4Da7D1](https://etherscan.io/address/0x5231E31C3ca39DD94fF56beCB662Ea50bC4Da7D1) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xaBd69D0f...fb81A9](https://etherscan.io/address/0xaBd69D0faC4b0851DAFe100979DF808Eb7fb81A9) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x699A8B3c...344073](https://etherscan.io/address/0x699A8B3cD08703359d78961dB51cabD872344073) | Frequent Token Sender | frequent_interactor | 50% |
| [0x288931fA...2b9FEf](https://etherscan.io/address/0x288931fA76d7B0482f0FD0BCA9a50Bf0D22b9FEf) | Frequent Token Sender | frequent_interactor | 50% |
| [0xDEF171Fe...6FEe57](https://etherscan.io/address/0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57) | Frequent Token Sender | frequent_interactor | 50% |
| [0x38F93078...d88fcb](https://etherscan.io/address/0x38F9307839A8E82b071EA6Fcbef029814Ed88fcb) | Frequent Token Sender | frequent_interactor | 50% |
| [0xBA71B56f...940513](https://etherscan.io/address/0xBA71B56fD0B590ED2a6992eD57a34C1391940513) | Frequent Token Sender | frequent_interactor | 50% |
| [0xF71530c1...210a8E](https://etherscan.io/address/0xF71530c1f043703085B42608ff9DCcCc43210a8E) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...0f594e](https://etherscan.io/address/0x000000000035B5e5ad9019092C665357240f594e) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...00dEaD](https://etherscan.io/address/0x000000000000000000000000000000000000dEaD) | Burn Address | burn | 100% |
| [0x00000000...00dead](https://etherscan.io/address/0x000000000000000000000000000000000000dead) | Burn Address | burn | 100% |
| [0x00000000...000000](https://etherscan.io/address/0x0000000000000000000000000000000000000000) | Burn Address | burn | 100% |


## TVL & Price History

| Metric | Value |
|--------|-------|
| Total TVL (in token units) | 12353.1798 |
| Active Pools | 0 |
| Main Pool | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) |
| Main Pool Share | 75.90% |


## Liquidity Events

- **Liquidity Additions:** 4 events
- **Liquidity Removals:** 15 events

### Significant Liquidity Removals

| Block | Timestamp | Pool | Actor | Amount0 | Amount1 |
|-------|-----------|------|-------|---------|---------|
| 15520913 | 2022-09-12 12:40:41 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 20.5749 | 277562386413.77 |
| 15562451 | 2022-09-18 19:15:47 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 38.2704 | 720691772546.15 |
| 15511055 | 2022-09-10 21:21:40 UTC | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 11290.1706 | 128.6298 |
| 15511057 | 2022-09-10 21:23:25 UTC | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 7011.2120 | 68.0526 |
| 15511060 | 2022-09-10 21:24:08 UTC | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 3676.1672 | 63.3700 |
| 15516470 | 2022-09-11 19:05:08 UTC | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 296.4976 | 0 |
| 15526086 | 2022-09-13 09:16:06 UTC | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 17.6683 | 55249929131.62 |
| 15638494 | 2022-09-29 10:45:47 UTC | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 5.0428 | 181054208264.03 |


## LP Concentration

| Metric | Value |
|--------|-------|
| Total LP Positions | 0 |
| Unique LPs | 0 |
| Top LP Share | 0.00% |
| Top 5 LP Share | 0.00% |


## Withdrawal Analysis

| Metric | Value |
|--------|-------|
| Pre-Crash Withdrawals | 15 |
| Attributed Withdrawals | 8 |
| Total Removed (FTX Token) | 22355.60379659 |
| Pre-Event TVL | 12353.1798 |
| Withdrawal Severity | 100.00% of pre-event TVL |

### Removals by Pool

| Pool | Events | Removed (FTX Token) | Est. USD | % Pool TVL |
|------|--------|--------------|----------|------------|
| [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | 6 | 22296.75856311 | - | 237.80% |
| [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | 2 | 58.84523347 | - | 9.68% |


## Incident Timeline

| Metric | Value |
|--------|-------|
| Total Events | 2207 |
| Swaps | 1078 |
| Liquidity Events | 34 |
| Block Range | 15504720 → 15711337 |
| Time Range | 2022-09-09 20:22:48 UTC → 2022-10-09 15:09:23 UTC |

### Alternative Cause Check

- Large token distributions detected — possible airdrop or coordinated sell.

### Key Events by Block

| Block | Timestamp | Event | Pool | Actor | Detail |
|-------|-----------|-------|------|-------|--------|
| 15697092 | 2022-10-07 15:23:59 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 20.9687 |
| 15697398 | 2022-10-07 16:26:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xB441F641...B3BC39](https://etherscan.io/address/0xB441F641874644A916EdeDe556B68BbcfFB3BC39) | Value: 2.0000 |
| 15697398 | 2022-10-07 16:26:59 UTC | SWAP (Swap) | [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 2.0000 |
| 15697528 | 2022-10-07 16:53:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xC170eCdf...2014aC](https://etherscan.io/address/0xC170eCdfB8c72681D3a170215Ea89b81A72014aC) | Value: 325009121857.87 |
| 15697528 | 2022-10-07 16:53:11 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 325009121857.87 |
| 15698882 | 2022-10-07 21:26:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Value: 2.0000 |
| 15698882 | 2022-10-07 21:26:59 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 2.0000 |
| 15699114 | 2022-10-07 22:13:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Value: 8.2976 |
| 15699114 | 2022-10-07 22:13:23 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 8.2976 |
| 15699281 | 2022-10-07 22:46:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Value: 6.0000 |
| 15699281 | 2022-10-07 22:46:59 UTC | SWAP (Swap) | [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | [0x11111112...43097d](https://etherscan.io/address/0x1111111254fb6c44bAC0beD2854e76F90643097d) | Amount0: 6.0000 |
| 15701044 | 2022-10-08 04:40:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x7825dE55...3E1bf3](https://etherscan.io/address/0x7825dE5586E4d2FD04459091bbe783fa243E1bf3) | Value: 11.4563 |
| 15701044 | 2022-10-08 04:40:47 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0x24902AA0...0000E0](https://etherscan.io/address/0x24902AA0cf0000a08c0EA0b003B0c0bF600000E0) | Amount0: 11.4563 |
| 15702279 | 2022-10-08 08:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x8D3543Fc...f1c45c](https://etherscan.io/address/0x8D3543Fcc1bA6a296f42dd52C2B7d33402f1c45c) | Value: 17.0000 |
| 15702279 | 2022-10-08 08:48:59 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xDef1C0de...b25EfF](https://etherscan.io/address/0xDef1C0ded9bec7F1a1670819833240f027b25EfF) | Amount0: 17.0000 |
| 15702967 | 2022-10-08 11:06:59 UTC | LIQUIDITY_REMOVE (Burn) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | Δ: 0 / 0 |
| 15702967 | 2022-10-08 11:06:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | Value: 5.4409 |
| 15702967 | 2022-10-08 11:06:59 UTC | COLLECT_FEES (Collect) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) |  |
| 15702982 | 2022-10-08 11:09:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xC56eEECf...1cFb57](https://etherscan.io/address/0xC56eEECf51ff5509D50EF91E79177c54d11cFb57) | Value: 5.4409 |
| 15702982 | 2022-10-08 11:09:59 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 5.4409 |
| 15704002 | 2022-10-08 14:34:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xd57b32b1...37D23b](https://etherscan.io/address/0xd57b32b12Cf8A62e20EF058b3ca1350E6937D23b) | Value: 3.8255 |
| 15704002 | 2022-10-08 14:34:35 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 3.8255 |
| 15704230 | 2022-10-08 15:20:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xbFB20e29...8C7415](https://etherscan.io/address/0xbFB20e29D0eA667ba8fD97203211f8D0328C7415) | Value: 1.7874 |
| 15704230 | 2022-10-08 15:20:23 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 1.7874 |
| 15706946 | 2022-10-09 00:26:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x94dA5D25...99B496](https://etherscan.io/address/0x94dA5D25947a70201BED03906432CB346F99B496) | Value: 5.4000 |
| 15706946 | 2022-10-09 00:26:11 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 5.4000 |
| 15710244 | 2022-10-09 11:29:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x5D954553...7d16B9](https://etherscan.io/address/0x5D9545534F97b9E010E1C8AFDA491718827d16B9) | Value: 4.1300 |
| 15710244 | 2022-10-09 11:29:11 UTC | SWAP (Swap) | [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | [0x11111112...43097d](https://etherscan.io/address/0x1111111254fb6c44bAC0beD2854e76F90643097d) | Amount0: 4.1300 |
| 15711337 | 2022-10-09 15:09:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x2b9da77F...01c482](https://etherscan.io/address/0x2b9da77F845e3CfD09e2F1F7bA136E324401c482) | Value: 10.4769 |
| 15711337 | 2022-10-09 15:09:23 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 10.4769 |


## Risk Feature Breakdown

| Feature | Value | Weight | Contribution | Description |
|---------|-------|--------|-------------|-------------|
| Pool Concentration | 0.7590 | 0.15 | 0.1138 | Main pool holds 75.90% of total DEX liquidity. |
| Lp Concentration | 0.0000 | 0.15 | 0.0000 | Largest LP holds 0.00% of pool shares. |
| Withdrawal Severity | 1.0000 | 0.20 | 0.2000 | Liquidity removed is 100.00% of reference TVL. |
| Temporal Proximity | 0.4500 | 0.15 | 0.0675 | No incident block — 15 liquidity removals in window. |
| Role Sensitivity | 0.8000 | 0.15 | 0.1200 | Deployer is directly involved in pool(s). |
| Market Impact | 0.0000 | 0.15 | 0.0000 | No incident block — market impact requires a crash reference. |
| Combined Activity | 1.0000 | 0.05 | 0.0500 | Suspicious activity: 15 withdrawals and large sells detected. |
| **Raw Score** | | | **0.5513** | |

### Interpretation

Some risk indicators are present, but the evidence is not conclusive.
Additional investigation into specific withdrawal patterns and address relationships
is recommended before drawing firm conclusions.


## Limitations & Caveats

1. **TVL estimates** for V3 Uniswap pools are approximate — actual liquidity is range-dependent.
2. **Price estimates** use simple AMM formulas and may not reflect actual trade prices.
3. **LP ownership** for V2 is reconstructed from Transfer events and may miss complex delegation patterns.
4. **V3 position analysis** is limited to visible PositionManager events.
5. **Alternative causes** (e.g., broader market events, exploits) are not exhaustively checked.
6. **Confidence scores** reflect data quality and completeness, not certainty of malicious intent.
7. A **high risk score indicates correlation, not causation** — always verify with independent data.

> **Important:** This report is for informational purposes. It does not constitute financial advice.


## Data Sources & Methodology

- **RPC Provider:** Ethereum mainnet via configured ETH_RPC_URL
- **Protocol Whitelist:** `config/protocols.ethereum.yaml`
- **Pool Discovery:** Factory getPair/getPool + event logs (PairCreated, PoolCreated)
- **Pool Verification:** On-chain factory, token pair, and event provenance checks
- **Event Indexing:** Chunked log queries with checkpoint/resume support
- **Position Reconstruction:** V2 LP-Transfer events; V3 PositionManager NFT ownership
- **Risk Model:** Weighted feature combination with migration adjustment

### Output Files

| File | Description |
|------|-------------|
| `token_profile.json` | Token metadata and behavior flags |
| `pool_candidates.json` | Raw pool discovery results |
| `verified_pools.json` | Verified pool addresses with confidence |
| `swaps.json` | Normalized swap events |
| `liquidity_events.json` | Normalized liquidity change events |
| Event tables | `swaps`, `liquidity_events`, and `transfers` (JSON and/or Parquet) |
| `positions.json` | LP position ownership |
| `address_labels.json` | Address role annotations |
| `metrics.json` | TVL, concentration, and withdrawal metrics |
| `incident_timeline.json` | Chronological event timeline |
| `risk_assessment.json` | Explainable risk score |
| `report.md` | This report |

