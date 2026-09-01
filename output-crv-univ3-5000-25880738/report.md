# On-Chain Token Crash & Liquidity Risk Report

## Executive Summary

- **Token:** CRV ([0xD533a949...34cd52](https://etherscan.io/address/0xD533a949740bb3306d119CC777fa900bA034cd52))
- **Chain:** Ethereum (Chain ID: 1)
- **Analysis Window:** Block 25875813 to 25880716
- **Incident Block:** Not specified
- **Report Generated:** 2026-09-01 09:09:02 UTC

### Risk Score

| Metric | Value |
|--------|-------|
| **Final Risk Score** | **0.1971 / 1.00** |
| **Risk Level** | **LOW** |
| Evidence Confidence | 73.00% |
| Visual | `███░░░░░░░░░░░░░░░░░` |


## Token Profile

| Property | Value |
|----------|-------|
| Address | [0xD533a949...34cd52](https://etherscan.io/address/0xD533a949740bb3306d119CC777fa900bA034cd52) |
| Symbol | CRV |
| Name | Curve DAO Token |
| Decimals | 18 (onchain) |
| Total Supply | 2414726890.3500 |
| Is Contract | True |
| Proxy Address | None |
| Implementation | None |
| Behavior Flags | minting |


## Pool Summary

**1** verified pool(s), **0** unverified candidate(s).

| Pool Address | Protocol | Version | Token0 | Token1 | Fee | Confidence |
|-------------|----------|---------|--------|--------|-----|------------|
| [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | uniswap | v3 | 0xC02aaA39... | 0xD533a949... | 3000 | 100.00% |


## Related Addresses

| Address | Label | Category | Confidence |
|---------|-------|----------|------------|
| [0x1F98431c...31F984](https://etherscan.io/address/0x1F98431c8aD98523631AE4a59f267346ea31F984) | Factory (uniswap)_v3 | protocol_deployment | 100% |
| [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | Uniswap V3 Pool | pool | 100% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | PositionManager (uniswap_v3) | position_manager | 100% |
| [0xE592427A...861564](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564) | Router (uniswap_v3) | router | 100% |
| [0xc4AD0Ef3...4B7Be4](https://etherscan.io/address/0xc4AD0Ef33A0A4ddA3461c479ccb6c36d1e4B7Be4) | Deployer | token_creator | 100% |
| [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x278d858f...6eF8D2](https://etherscan.io/address/0x278d858f05b94576C1E6f73285886876ff6eF8D2) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xBdb3ba9f...DF47B6](https://etherscan.io/address/0xBdb3ba9ffe392549E1f8658DD2630c141fDF47B6) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xEff6cb8b...1aA167](https://etherscan.io/address/0xEff6cb8b614999d130E537751Ee99724D01aA167) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111605...305Afe](https://etherscan.io/address/0x11111605ef067242653c980B8f6F1ffE50305Afe) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...E08A90](https://etherscan.io/address/0x000000000004444c5dc75cB358380D2e3dE08A90) | Frequent Token Sender | frequent_interactor | 50% |
| [0x229965B0...DcD340](https://etherscan.io/address/0x229965B0ee9ED33450317E6725edEC3909DcD340) | Frequent Token Sender | frequent_interactor | 50% |
| [0x3d407EF8...2F5e63](https://etherscan.io/address/0x3d407EF8378336Da0208F41c4adFeEb4822F5e63) | Frequent Token Sender | frequent_interactor | 50% |
| [0xc1D0465F...fb1aBA](https://etherscan.io/address/0xc1D0465FF243fEcE2856Eac534C16cf1C8fb1aBA) | Frequent Token Sender | frequent_interactor | 50% |
| [0xf1d1ABa8...f9D410](https://etherscan.io/address/0xf1d1ABa8BD488c0f0b1EA4D2085b243091f9D410) | Frequent Token Sender | frequent_interactor | 50% |
| [0x55d8586b...e3dC31](https://etherscan.io/address/0x55d8586b5C03b74122A772c24b7307dB8Be3dC31) | Frequent Token Sender | frequent_interactor | 50% |
| [0xE08D97e1...72D015](https://etherscan.io/address/0xE08D97e151473A848C3d9CA3f323Cb720472D015) | Frequent Token Sender | frequent_interactor | 50% |
| [0x1f2F10D1...6Df387](https://etherscan.io/address/0x1f2F10D1C40777AE1Da742455c65828FF36Df387) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...00dEaD](https://etherscan.io/address/0x000000000000000000000000000000000000dEaD) | Burn Address | burn | 100% |
| [0x00000000...00dead](https://etherscan.io/address/0x000000000000000000000000000000000000dead) | Burn Address | burn | 100% |
| [0x00000000...000000](https://etherscan.io/address/0x0000000000000000000000000000000000000000) | Burn Address | burn | 100% |


## TVL & Price History

| Metric | Value |
|--------|-------|
| Total TVL (in token units) | 1883568.5280 |
| Active Pools | 0 |
| Main Pool | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) |
| Main Pool Share | 100.00% |


## Liquidity Events

- **Liquidity Additions:** 1 events
- **Liquidity Removals:** 0 events


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
| Pre-Crash Withdrawals | 0 |
| Attributed Withdrawals | 0 |
| Total Removed (CRV) | 0.0 |
| Pre-Event TVL | 1883568.5280 |
| Withdrawal Severity | 0.00% of pre-event TVL |


## Incident Timeline

| Metric | Value |
|--------|-------|
| Total Events | 1066 |
| Swaps | 532 |
| Liquidity Events | 1 |
| Block Range | 25875813 → 25880716 |
| Time Range | 2026-08-31 14:19:23 UTC → 2026-09-01 06:44:11 UTC |

### Alternative Cause Check

- Large token distributions detected — possible airdrop or coordinated sell.

### Key Events by Block

| Block | Timestamp | Event | Pool | Actor | Detail |
|-------|-----------|-------|------|-------|--------|
| 25880637 | 2026-09-01 06:28:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Value: 50.4929 |
| 25880637 | 2026-09-01 06:28:23 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Amount0: 7140174594.18 |
| 25880639 | 2026-09-01 06:28:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xE08D97e1...72D015](https://etherscan.io/address/0xE08D97e151473A848C3d9CA3f323Cb720472D015) | Value: 50.4929 |
| 25880639 | 2026-09-01 06:28:47 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0xE08D97e1...72D015](https://etherscan.io/address/0xE08D97e151473A848C3d9CA3f323Cb720472D015) | Amount0: 7138982855.75 |
| 25880643 | 2026-09-01 06:29:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | Value: 22723908627.43 |
| 25880643 | 2026-09-01 06:29:35 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0xD1c6aca7...90c7Eb](https://etherscan.io/address/0xD1c6aca7eA7eD44E1873dAFa054c28Ceb690c7Eb) | Amount0: 3231934.80 |
| 25880643 | 2026-09-01 06:29:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Value: 50.4929 |
| 25880643 | 2026-09-01 06:29:35 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Amount0: 7137791953.39 |
| 25880647 | 2026-09-01 06:30:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | Value: 1470.4314 |
| 25880647 | 2026-09-01 06:30:23 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0xCbC35d5c...07Dde6](https://etherscan.io/address/0xCbC35d5c850a94Bf4866b768A72FA688dB07Dde6) | Amount0: 209609852763.92 |
| 25880647 | 2026-09-01 06:30:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Value: 50.4929 |
| 25880647 | 2026-09-01 06:30:23 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Amount0: 7171516334.99 |
| 25880648 | 2026-09-01 06:30:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x73851bF6...51c3E5](https://etherscan.io/address/0x73851bF6c6E49cC44A1680451A127795C951c3E5) | Value: 50.4929 |
| 25880648 | 2026-09-01 06:30:35 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x73851bF6...51c3E5](https://etherscan.io/address/0x73851bF6c6E49cC44A1680451A127795C951c3E5) | Amount0: 7170316741.59 |
| 25880648 | 2026-09-01 06:30:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Value: 50.4929 |
| 25880648 | 2026-09-01 06:30:35 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Amount0: 7169117449.15 |
| 25880648 | 2026-09-01 06:30:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Value: 50.4929 |
| 25880648 | 2026-09-01 06:30:35 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Amount0: 7167918457.57 |
| 25880652 | 2026-09-01 06:31:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Value: 50.4929 |
| 25880652 | 2026-09-01 06:31:23 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Amount0: 7166719766.76 |
| 25880652 | 2026-09-01 06:31:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Value: 50.4929 |
| 25880652 | 2026-09-01 06:31:23 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Amount0: 7165521376.60 |
| 25880653 | 2026-09-01 06:31:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xBdb3ba9f...DF47B6](https://etherscan.io/address/0xBdb3ba9ffe392549E1f8658DD2630c141fDF47B6) | Value: 368.7238 |
| 25880653 | 2026-09-01 06:31:35 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0xBdb3ba9f...DF47B6](https://etherscan.io/address/0xBdb3ba9ffe392549E1f8658DD2630c141fDF47B6) | Amount0: 52289850469.39 |
| 25880654 | 2026-09-01 06:31:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x278d858f...6eF8D2](https://etherscan.io/address/0x278d858f05b94576C1E6f73285886876ff6eF8D2) | Value: 225.5686 |
| 25880654 | 2026-09-01 06:31:47 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x278d858f...6eF8D2](https://etherscan.io/address/0x278d858f05b94576C1E6f73285886876ff6eF8D2) | Amount0: 31957124415.78 |
| 25880706 | 2026-09-01 06:42:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x229965B0...DcD340](https://etherscan.io/address/0x229965B0ee9ED33450317E6725edEC3909DcD340) | Value: 231.8720 |
| 25880706 | 2026-09-01 06:42:11 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x229965B0...DcD340](https://etherscan.io/address/0x229965B0ee9ED33450317E6725edEC3909DcD340) | Amount0: 32825294342.43 |
| 25880716 | 2026-09-01 06:44:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Value: 416486205358.02 |
| 25880716 | 2026-09-01 06:44:11 UTC | SWAP (Swap) | [0x919Fa96e...cDaf79](https://etherscan.io/address/0x919Fa96e88d67499339577Fa202345436bcDaf79) | [0x00000F91...8A0CAc](https://etherscan.io/address/0x00000F91109c4d0007e90000D9facAD5298A0CAc) | Amount0: 58937832.03 |


## Risk Feature Breakdown

| Feature | Value | Weight | Contribution | Description |
|---------|-------|--------|-------------|-------------|
| Pool Concentration | 1.0000 | 0.15 | 0.1500 | Main pool holds 100.00% of total DEX liquidity. |
| Lp Concentration | 0.0000 | 0.15 | 0.0000 | Largest LP holds 0.00% of pool shares. |
| Withdrawal Severity | 0.0000 | 0.20 | 0.0000 | Liquidity removed is 0.00% of reference TVL. |
| Temporal Proximity | 0.0000 | 0.15 | 0.0000 | No withdrawals to evaluate. |
| Role Sensitivity | 0.8000 | 0.15 | 0.1200 | Deployer is directly involved in pool(s). |
| Market Impact | 0.0000 | 0.15 | 0.0000 | No incident block — market impact requires a crash reference. |
| Combined Activity | 0.0000 | 0.05 | 0.0000 | Suspicious activity: 0 withdrawals. |
| **Raw Score** | | | **0.2700** | |

### Interpretation

The available evidence suggests **low risk** of a liquidity-attributable crash.
The market impact may be driven by normal trading activity or external factors.


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
