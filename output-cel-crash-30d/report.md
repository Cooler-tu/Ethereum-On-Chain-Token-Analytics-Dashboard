# On-Chain Token Crash & Liquidity Risk Report

## Executive Summary

- **Token:** CEL ([0xaaAEBE6F...09D42d](https://etherscan.io/address/0xaaAEBE6Fe48E54f431b0C390CfaF0b017d09D42d))
- **Chain:** Ethereum (Chain ID: 1)
- **Analysis Window:** Block 14771025 to 14953472
- **Incident Block:** 14953505
- **Report Generated:** 2026-08-27 05:47:23 UTC

### Risk Score

| Metric | Value |
|--------|-------|
| **Final Risk Score** | **0.3738 / 1.00** |
| **Risk Level** | **LOW** |
| Evidence Confidence | 91.00% |
| Visual | `███████░░░░░░░░░░░░░` |


## Token Profile

| Property | Value |
|----------|-------|
| Address | [0xaaAEBE6F...09D42d](https://etherscan.io/address/0xaaAEBE6Fe48E54f431b0C390CfaF0b017d09D42d) |
| Symbol | CEL |
| Name | Celsius |
| Decimals | 4 (onchain) |
| Total Supply | 357191.26 |
| Is Contract | True |
| Proxy Address | None |
| Implementation | None |
| Behavior Flags | None |


## Pool Summary

**2** verified pool(s), **0** unverified candidate(s).

| Pool Address | Protocol | Version | Token0 | Token1 | Fee | Confidence |
|-------------|----------|---------|--------|--------|-----|------------|
| [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | uniswap | v2 | 0xaaAEBE6F... | 0xC02aaA39... | N/A | 100.00% |
| [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) | uniswap | v3 | 0xaaAEBE6F... | 0xC02aaA39... | 3000 | 100.00% |


## Related Addresses

| Address | Label | Category | Confidence |
|---------|-------|----------|------------|
| [0x5C69bEe7...c5aA6f](https://etherscan.io/address/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f) | Factory (uniswap)_v2 | protocol_deployment | 100% |
| [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | Uniswap V2 Pool | pool | 100% |
| [0x7a250d56...F2488D](https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D) | Router (uniswap_v2) | router | 100% |
| [0x1F98431c...31F984](https://etherscan.io/address/0x1F98431c8aD98523631AE4a59f267346ea31F984) | Factory (uniswap)_v3 | protocol_deployment | 100% |
| [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) | Uniswap V3 Pool | pool | 100% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | PositionManager (uniswap_v3) | position_manager | 100% |
| [0xE592427A...861564](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564) | Router (uniswap_v3) | router | 100% |
| [0xAd8b03BB...5EAFC9](https://etherscan.io/address/0xAd8b03BB5576f31Ff3fD29ebdA4D5d920a5EAFC9) | Deployer | token_creator | 100% |
| [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x8aFF5cA9...455580](https://etherscan.io/address/0x8aFF5cA996F77487a4f04F1ce905Bf3d27455580) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xe66B3167...133750](https://etherscan.io/address/0xe66B31678d6C16E9ebf358268a790B763C133750) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xa3B83D0E...aBCa16](https://etherscan.io/address/0xa3B83D0E2F3d2C675439188eF1aa13D1C6aBCa16) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x00000000...5e9f56](https://etherscan.io/address/0x0000000000007F150Bd6f54c40A34d7C3d5e9f56) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x00000000...0f594e](https://etherscan.io/address/0x000000000035B5e5ad9019092C665357240f594e) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x6e4182C1...5dd319](https://etherscan.io/address/0x6e4182C1de5Fe878C019f518d3d7b6444e5dd319) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x437Ae281...98622F](https://etherscan.io/address/0x437Ae28150189890d987Deee46CC29BF4098622F) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x0000d2FA...B02a81](https://etherscan.io/address/0x0000d2FA2D0000A58C0000c300720b0ee3B02a81) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x8faC5A19...403995](https://etherscan.io/address/0x8faC5A19B2432fda01bfFeE8b3CC5AE073403995) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x00000000...0f9e75](https://etherscan.io/address/0x00000000AE347930bD1E7B0F35588b92280f9e75) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x0000E0Ca...000000](https://etherscan.io/address/0x0000E0Ca771e21bD00057F54A68C30D400000000) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x45716d9E...71B20F](https://etherscan.io/address/0x45716d9EDdbc332df1D42b9F540FBEBeD671B20F) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x41163e3F...177E45](https://etherscan.io/address/0x41163e3F165F3eF840AE7754D4031aad01177E45) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x09ea7680...E5E450](https://etherscan.io/address/0x09ea768029069EEB979015a64f261e7789E5E450) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x4A9Db201...8B376A](https://etherscan.io/address/0x4A9Db20153506e45EdBC95850Af056C4258B376A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x58418d6c...E77DbA](https://etherscan.io/address/0x58418d6c83EfAB01ed78b0AC42E55af01eE77DbA) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x220bdA5c...2196D4](https://etherscan.io/address/0x220bdA5c8994804Ac96ebe4DF184d25e5c2196D4) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x954F1943...F7D25d](https://etherscan.io/address/0x954F1943Af6f46971ee4C81E73f9103359F7D25d) | Frequent Token Sender | frequent_interactor | 50% |
| [0x8700eB98...A85eca](https://etherscan.io/address/0x8700eB9899d773A251e434746b94b49e25A85eca) | Frequent Token Sender | frequent_interactor | 50% |
| [0xe1f08D77...147c2D](https://etherscan.io/address/0xe1f08D771FB7B248B3266B7F79A9eAfBA3147c2D) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...91e2D4](https://etherscan.io/address/0x000000000dFDe7deaF24138722987c9a6991e2D4) | Frequent Token Sender | frequent_interactor | 50% |
| [0xDEF171Fe...6FEe57](https://etherscan.io/address/0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57) | Frequent Token Sender | frequent_interactor | 50% |
| [0xbaDc0dEf...fCF05A](https://etherscan.io/address/0xbaDc0dEfAfCF6d4239BDF0b66da4D7Bd36fCF05A) | Frequent Token Sender | frequent_interactor | 50% |
| [0x0000006d...7Fb793](https://etherscan.io/address/0x0000006daea1723962647b7e189d311d757Fb793) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...00dead](https://etherscan.io/address/0x000000000000000000000000000000000000dead) | Burn Address | burn | 100% |
| [0x00000000...00dEaD](https://etherscan.io/address/0x000000000000000000000000000000000000dEaD) | Burn Address | burn | 100% |
| [0x00000000...000000](https://etherscan.io/address/0x0000000000000000000000000000000000000000) | Burn Address | burn | 100% |


## TVL & Price History

| Metric | Value |
|--------|-------|
| Total TVL (in token units) | 24985.51 |
| Active Pools | 0 |
| Main Pool | [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) |
| Main Pool Share | 81.45% |


## Liquidity Events

- **Liquidity Additions:** 21 events
- **Liquidity Removals:** 32 events


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
| Pre-Crash Withdrawals | 32 |
| Attributed Withdrawals | 23 |
| Total Removed (CEL) | 295088.3453 |
| Pre-Event TVL | 24985.51 |
| Withdrawal Severity | 11.81% of pre-event TVL |

### Removals by Pool

| Pool | Events | Removed (CEL) | Est. USD | % Pool TVL |
|------|--------|--------------|----------|------------|
| [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) | 18 | 286618.0712 | - | 14.08% |
| [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | 5 | 8470.2741 | - | 1.83% |


## Incident Timeline

| Metric | Value |
|--------|-------|
| Total Events | 9891 |
| Swaps | 4972 |
| Liquidity Events | 78 |
| Block Range | 14771025 → 14953472 |
| Time Range | 2022-05-14 02:16:54 UTC → 2022-06-13 02:03:37 UTC |

### Alternative Cause Check

- Large token distributions detected — possible airdrop or coordinated sell.

### Key Events by Block

| Block | Timestamp | Event | Pool | Actor | Detail |
|-------|-----------|-------|------|-------|--------|
| 14953413 | 2022-06-13 01:50:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | Value: 5.78 |
| 14953413 | 2022-06-13 01:50:35 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x00000000...416B40](https://etherscan.io/address/0x00000000003b3cc22aF3aE1EAc0440BcEe416B40) | Amount0: -5776911 |
| 14953413 | 2022-06-13 01:50:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | Value: 78.44 |
| 14953413 | 2022-06-13 01:50:35 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: -78441046 |
| 14953413 | 2022-06-13 01:50:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000000...416B40](https://etherscan.io/address/0x00000000003b3cc22aF3aE1EAc0440BcEe416B40) | Value: 5.78 |
| 14953413 | 2022-06-13 01:50:35 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x00000000...416B40](https://etherscan.io/address/0x00000000003b3cc22aF3aE1EAc0440BcEe416B40) | Amount0: 5.78 |
| 14953417 | 2022-06-13 01:51:16 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x954F1943...F7D25d](https://etherscan.io/address/0x954F1943Af6f46971ee4C81E73f9103359F7D25d) | Value: 40.96 |
| 14953417 | 2022-06-13 01:51:16 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x563bDabA...0a02Ed](https://etherscan.io/address/0x563bDabAa8846ec445b25Bfbed88d160890a02Ed) | Amount0: 40.96 |
| 14953426 | 2022-06-13 01:53:44 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | Value: 234.19 |
| 14953426 | 2022-06-13 01:53:44 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x7a250d56...F2488D](https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D) | Amount0: -234185519 |
| 14953426 | 2022-06-13 01:53:44 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x954F1943...F7D25d](https://etherscan.io/address/0x954F1943Af6f46971ee4C81E73f9103359F7D25d) | Value: 149.33 |
| 14953426 | 2022-06-13 01:53:44 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x0000E0Ca...000000](https://etherscan.io/address/0x0000E0Ca771e21bD00057F54A68C30D400000000) | Amount0: 149.33 |
| 14953427 | 2022-06-13 01:54:08 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x6e4182C1...5dd319](https://etherscan.io/address/0x6e4182C1de5Fe878C019f518d3d7b6444e5dd319) | Value: 32.92 |
| 14953427 | 2022-06-13 01:54:08 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0xB23DC3F0...75aA4C](https://etherscan.io/address/0xB23DC3F00856288Cd7B6Bde5D06159f01b75aA4C) | Amount0: 32.92 |
| 14953431 | 2022-06-13 01:54:25 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) | Value: 21.00 |
| 14953431 | 2022-06-13 01:54:25 UTC | SWAP (Swap) | [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) | [0x0027003e...eCC200](https://etherscan.io/address/0x0027003e0039314E90B8600000006a081deCC200) | Amount0: 21.00 |
| 14953433 | 2022-06-13 01:55:10 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x220bdA5c...2196D4](https://etherscan.io/address/0x220bdA5c8994804Ac96ebe4DF184d25e5c2196D4) | Value: 30.00 |
| 14953433 | 2022-06-13 01:55:10 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x220bdA5c...2196D4](https://etherscan.io/address/0x220bdA5c8994804Ac96ebe4DF184d25e5c2196D4) | Amount0: 30.00 |
| 14953437 | 2022-06-13 01:55:32 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x220bdA5c...2196D4](https://etherscan.io/address/0x220bdA5c8994804Ac96ebe4DF184d25e5c2196D4) | Value: 17.78 |
| 14953437 | 2022-06-13 01:55:32 UTC | SWAP (Swap) | [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) | [0x220bdA5c...2196D4](https://etherscan.io/address/0x220bdA5c8994804Ac96ebe4DF184d25e5c2196D4) | Amount0: 17.78 |
| 14953437 | 2022-06-13 01:55:32 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x220bdA5c...2196D4](https://etherscan.io/address/0x220bdA5c8994804Ac96ebe4DF184d25e5c2196D4) | Value: 19.26 |
| 14953437 | 2022-06-13 01:55:32 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x220bdA5c...2196D4](https://etherscan.io/address/0x220bdA5c8994804Ac96ebe4DF184d25e5c2196D4) | Amount0: 19.26 |
| 14953450 | 2022-06-13 01:58:30 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x2057CfB9...E7189A](https://etherscan.io/address/0x2057CfB9fD11837D61B294D514C5bd03e5E7189A) | Value: 122.21 |
| 14953450 | 2022-06-13 01:58:30 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0x2057CfB9...E7189A](https://etherscan.io/address/0x2057CfB9fD11837D61B294D514C5bd03e5E7189A) | Amount0: 122.21 |
| 14953450 | 2022-06-13 01:58:30 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | Value: 51.51 |
| 14953450 | 2022-06-13 01:58:30 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0xED35DF87...F02639](https://etherscan.io/address/0xED35DF87B50044C3E3133a1F7297659851F02639) | Amount0: -51514043 |
| 14953451 | 2022-06-13 01:59:09 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x954F1943...F7D25d](https://etherscan.io/address/0x954F1943Af6f46971ee4C81E73f9103359F7D25d) | Value: 14.25 |
| 14953451 | 2022-06-13 01:59:09 UTC | SWAP (Swap) | [0x06729eb2...DE5105](https://etherscan.io/address/0x06729eb2424da47898F935267BD4a62940DE5105) | [0xB23DC3F0...75aA4C](https://etherscan.io/address/0xB23DC3F00856288Cd7B6Bde5D06159f01b75aA4C) | Amount0: 14.25 |
| 14953467 | 2022-06-13 02:02:53 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | Value: 13.15 |
| 14953467 | 2022-06-13 02:02:53 UTC | SWAP (Swap) | [0xa5E79baE...7d9Fe6](https://etherscan.io/address/0xa5E79baEe540f000ef6F23D067cd3AC22c7d9Fe6) | [0xDEF171Fe...6FEe57](https://etherscan.io/address/0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57) | Amount0: -13147014 |


## Risk Feature Breakdown

| Feature | Value | Weight | Contribution | Description |
|---------|-------|--------|-------------|-------------|
| Pool Concentration | 0.8145 | 0.15 | 0.1222 | Main pool holds 81.45% of total DEX liquidity. |
| Lp Concentration | 0.0000 | 0.15 | 0.0000 | Largest LP holds 0.00% of pool shares. |
| Withdrawal Severity | 0.1181 | 0.20 | 0.0236 | Liquidity removed is 11.81% of reference TVL. |
| Temporal Proximity | 0.8000 | 0.15 | 0.1200 | Withdrawal within 6 hours of crash |
| Role Sensitivity | 0.8000 | 0.15 | 0.1200 | Deployer is directly involved in pool(s). |
| Market Impact | 0.0000 | 0.15 | 0.0000 | No significant price change detected. |
| Combined Activity | 0.5000 | 0.05 | 0.0250 | Suspicious activity: 32 withdrawals. |
| **Raw Score** | | | **0.4108** | |

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

