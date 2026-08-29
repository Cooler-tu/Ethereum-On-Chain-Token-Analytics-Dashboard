# On-Chain Token Crash & Liquidity Risk Report

## Executive Summary

- **Token:** GALA ([0xd1d2Eb1B...C87cae](https://etherscan.io/address/0xd1d2Eb1B1e90B638588728b4130137D262C87cae))
- **Chain:** Ethereum (Chain ID: 1)
- **Analysis Window:** Block 19913247 to 20127797
- **Incident Block:** Not specified
- **Report Generated:** 2026-08-29 09:42:11 UTC

### Risk Score

| Metric | Value |
|--------|-------|
| **Final Risk Score** | **0.2355 / 1.00** |
| **Risk Level** | **LOW** |
| Evidence Confidence | 91.00% |
| Visual | `████░░░░░░░░░░░░░░░░` |
| Migration Adjustment | Liquidity migration detected — reducing risk by 0.30. |


## Token Profile

| Property | Value |
|----------|-------|
| Address | [0xd1d2Eb1B...C87cae](https://etherscan.io/address/0xd1d2Eb1B1e90B638588728b4130137D262C87cae) |
| Symbol | GALA |
| Name | Gala |
| Decimals | 8 (onchain) |
| Total Supply | 4.4798 |
| Is Contract | True |
| Proxy Address | 0xd1d2Eb1B1e90B638588728b4130137D262C87cae |
| Implementation | 0x8D92A6812b3dA2346883F0631910c96Cb9c5a5f9 |
| Behavior Flags | None |


## Pool Summary

**2** verified pool(s), **0** unverified candidate(s).

| Pool Address | Protocol | Version | Token0 | Token1 | Fee | Confidence |
|-------------|----------|---------|--------|--------|-----|------------|
| [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | uniswap | v2 | 0xC02aaA39... | 0xd1d2Eb1B... | N/A | 100.00% |
| [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | uniswap | v3 | 0xC02aaA39... | 0xd1d2Eb1B... | 3000 | 100.00% |


## Related Addresses

| Address | Label | Category | Confidence |
|---------|-------|----------|------------|
| [0x5C69bEe7...c5aA6f](https://etherscan.io/address/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f) | Factory (uniswap)_v2 | protocol_deployment | 100% |
| [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | Uniswap V2 Pool | pool | 100% |
| [0x7a250d56...F2488D](https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D) | Router (uniswap_v2) | router | 100% |
| [0x1F98431c...31F984](https://etherscan.io/address/0x1F98431c8aD98523631AE4a59f267346ea31F984) | Factory (uniswap)_v3 | protocol_deployment | 100% |
| [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | Uniswap V3 Pool | pool | 100% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | PositionManager (uniswap_v3) | position_manager | 100% |
| [0xE592427A...861564](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564) | Router (uniswap_v3) | router | 100% |
| [0xdaE4249f...4C9f26](https://etherscan.io/address/0xdaE4249fA57610723B1f1B1c0379897aED4C9f26) | Deployer | token_creator | 100% |
| [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x3fC91A3a...2b7FAD](https://etherscan.io/address/0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xf5213a6a...1A9900](https://etherscan.io/address/0xf5213a6a2f0890321712520b8048D9886c1A9900) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x98C3d318...8d6B8E](https://etherscan.io/address/0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x22F9dCF4...178C18](https://etherscan.io/address/0x22F9dCF4647084d6C31b2765F6910cd85C178C18) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...43097d](https://etherscan.io/address/0x1111111254fb6c44bAC0beD2854e76F90643097d) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xa7Ca2C86...0Db22A](https://etherscan.io/address/0xa7Ca2C8673bcFA5a26d8ceeC2887f2CC2b0Db22A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xc6feCDF7...f8Bae1](https://etherscan.io/address/0xc6feCDF760Af24095cDEd954dE7d81aB49f8Bae1) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x00000000...120E49](https://etherscan.io/address/0x00000000009E50a7dDb7a7B0e2ee6604fd120E49) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x525145f8...17F7cb](https://etherscan.io/address/0x525145f821D8D2ABb494c454E9445E14c817F7cb) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xf081470f...DcdD67](https://etherscan.io/address/0xf081470f5C6FBCCF48cC4e5B82Dd926409DcdD67) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...842A65](https://etherscan.io/address/0x111111125421cA6dc452d289314280a0f8842A65) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x0D59b9D6...6dcF65](https://etherscan.io/address/0x0D59b9D6978814eC27C4D3426949F5373f6dcF65) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xE37e799D...57BD09](https://etherscan.io/address/0xE37e799D5077682FA0a244D46E5649F71457BD09) | Frequent Token Sender | frequent_interactor | 50% |
| [0xe2Ca4711...100F97](https://etherscan.io/address/0xe2Ca471124b124831e231fb835778840Ad100F97) | Frequent Token Sender | frequent_interactor | 50% |
| [0x9008D19f...60ab41](https://etherscan.io/address/0x9008D19f58AAbD9eD0D60971565AA8510560ab41) | Frequent Token Sender | frequent_interactor | 50% |
| [0x000000fe...2E7E1c](https://etherscan.io/address/0x000000fee13a103A10D593b9AE06b3e05F2E7E1c) | Frequent Token Sender | frequent_interactor | 50% |
| [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Frequent Token Sender | frequent_interactor | 50% |
| [0xb1b2d032...6E8404](https://etherscan.io/address/0xb1b2d032AA2F52347fbcfd08E5C3Cc55216E8404) | Frequent Token Sender | frequent_interactor | 50% |
| [0xe43ca1De...1A59F5](https://etherscan.io/address/0xe43ca1Dee3F0fc1e2df73A0745674545F11A59F5) | Frequent Token Sender | frequent_interactor | 50% |
| [0xad3b67BC...4A968f](https://etherscan.io/address/0xad3b67BCA8935Cb510C8D18bD45F0b94F54A968f) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...000000](https://etherscan.io/address/0x0000000000000000000000000000000000000000) | Burn Address | burn | 100% |
| [0x00000000...00dead](https://etherscan.io/address/0x000000000000000000000000000000000000dead) | Burn Address | burn | 100% |
| [0x00000000...00dEaD](https://etherscan.io/address/0x000000000000000000000000000000000000dEaD) | Burn Address | burn | 100% |


## TVL & Price History

| Metric | Value |
|--------|-------|
| Total TVL (in token units) | 7634038791.99 |
| Active Pools | 0 |
| Main Pool | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) |
| Main Pool Share | 97.52% |


## Liquidity Events

- **Liquidity Additions:** 128 events
- **Liquidity Removals:** 136 events

### Significant Liquidity Removals

| Block | Timestamp | Pool | Actor | Amount0 | Amount1 |
|-------|-----------|------|-------|---------|---------|
| 19913786 | 2024-05-20 21:23:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 2.2005 | 57712353.25 |
| 19913947 | 2024-05-20 21:55:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 7.8645 | 36894883.08 |
| 19913954 | 2024-05-20 21:56:59 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 2.0000 | 0 |
| 19913970 | 2024-05-20 22:00:11 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 9.3000 | 0 |
| 19914046 | 2024-05-20 22:15:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 104.4845 | 105103394.70 |
| 19914053 | 2024-05-20 22:16:47 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 467.9441 | 80060500.98 |
| 19914069 | 2024-05-20 22:19:59 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 11.7447 | 0 |
| 19914149 | 2024-05-20 22:36:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 3.9923 | 21949649.24 |
| 19914191 | 2024-05-20 22:44:47 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 9.0000 | 0 |
| 19914387 | 2024-05-20 23:24:11 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 4.6705 | 0 |
| 19914387 | 2024-05-20 23:24:11 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 16.6780 | 14603165.47 |
| 19914673 | 2024-05-21 00:22:11 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 489.2496 | 44666817.96 |
| 19916152 | 2024-05-21 05:19:47 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 1.3566 | 16814026.60 |
| 19917019 | 2024-05-21 08:13:59 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | 25.6408 | 568415243.03 |
| 19917567 | 2024-05-21 10:04:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 6.8097 | 19193304.68 |
| 19917569 | 2024-05-21 10:04:47 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 9.9580 | 374658.22 |
| 19920934 | 2024-05-21 21:21:47 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 4.2399 | 0 |
| 19920975 | 2024-05-21 21:29:59 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 9.5081 | 0 |
| 19921111 | 2024-05-21 21:57:11 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 9.0000 | 0 |
| 19921512 | 2024-05-21 23:17:47 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | 16.8014 | 318733981.37 |


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
| Pre-Crash Withdrawals | 136 |
| Attributed Withdrawals | 102 |
| Total Removed (GALA) | 129260810.41485727 |
| Pre-Event TVL | 7634038791.99 |
| Withdrawal Severity | 100.00% of pre-event TVL |

### Removals by Pool

| Pool | Events | Removed (GALA) | Est. USD | % Pool TVL |
|------|--------|--------------|----------|------------|
| [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | 102 | 129260810.41485727 | - | 173.63% |


## Incident Timeline

| Metric | Value |
|--------|-------|
| Total Events | 14590 |
| Swaps | 7022 |
| Liquidity Events | 398 |
| Block Range | 19913247 → 20127797 |
| Time Range | 2024-05-20 19:35:11 UTC → 2024-06-19 19:12:59 UTC |

### Liquidity Migration Detected

The following migration candidates were found:
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19913947) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19913947)
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19913970) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19913973)
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19914046) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19914046)
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19914053) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19914053)
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19914069) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19914069)

### Alternative Cause Check

- Large token distributions detected — possible airdrop or coordinated sell.

### Key Events by Block

| Block | Timestamp | Event | Pool | Actor | Detail |
|-------|-----------|-------|------|-------|--------|
| 20126866 | 2024-06-19 16:05:47 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x3fC91A3a...2b7FAD](https://etherscan.io/address/0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD) | Amount0: 319106916499.05 |
| 20126866 | 2024-06-19 16:05:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | Value: 6843030.72 |
| 20126866 | 2024-06-19 16:05:47 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 539191500133.06 |
| 20126981 | 2024-06-19 16:28:47 UTC | LIQUIDITY_REMOVE (Burn) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | Δ: 0 / 885497.29 |
| 20126981 | 2024-06-19 16:28:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | Value: 951305.60 |
| 20126981 | 2024-06-19 16:28:47 UTC | COLLECT_FEES (Collect) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) |  |
| 20127154 | 2024-06-19 17:03:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | Value: 124648.06 |
| 20127154 | 2024-06-19 17:03:35 UTC | SWAP (Swap) | [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Amount0: 9912500000.00 |
| 20127198 | 2024-06-19 17:12:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xa7Ca2C86...0Db22A](https://etherscan.io/address/0xa7Ca2C8673bcFA5a26d8ceeC2887f2CC2b0Db22A) | Value: 1384183.06 |
| 20127198 | 2024-06-19 17:12:35 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Amount0: 108756596028.35 |
| 20127211 | 2024-06-19 17:15:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | Value: 7086602.85 |
| 20127211 | 2024-06-19 17:15:11 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Amount0: 562023282323.36 |
| 20127252 | 2024-06-19 17:23:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | Value: 6147549.41 |
| 20127252 | 2024-06-19 17:23:23 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xcB83cA96...Ad4472](https://etherscan.io/address/0xcB83cA9633Ad057Bd88A48a5B6e8108D97Ad4472) | Amount0: 491329408630.67 |
| 20127254 | 2024-06-19 17:23:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xE37e799D...57BD09](https://etherscan.io/address/0xE37e799D5077682FA0a244D46E5649F71457BD09) | Value: 995.00 |
| 20127254 | 2024-06-19 17:23:47 UTC | SWAP (Swap) | [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | [0xE37e799D...57BD09](https://etherscan.io/address/0xE37e799D5077682FA0a244D46E5649F71457BD09) | Amount0: -78755332489665 |
| 20127368 | 2024-06-19 17:46:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | Value: 248319.01 |
| 20127368 | 2024-06-19 17:46:59 UTC | SWAP (Swap) | [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Amount0: 19825000000.00 |
| 20127405 | 2024-06-19 17:54:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xE37e799D...57BD09](https://etherscan.io/address/0xE37e799D5077682FA0a244D46E5649F71457BD09) | Value: 362039.95 |
| 20127405 | 2024-06-19 17:54:23 UTC | SWAP (Swap) | [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | [0xE37e799D...57BD09](https://etherscan.io/address/0xE37e799D5077682FA0a244D46E5649F71457BD09) | Amount0: -28697020740577502 |
| 20127414 | 2024-06-19 17:56:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x74EA14Fe...a77b6a](https://etherscan.io/address/0x74EA14Fe1c5E085dcca2CfFDd2712d475Ea77b6a) | Value: 1900000.00 |
| 20127414 | 2024-06-19 17:56:11 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x3fC91A3a...2b7FAD](https://etherscan.io/address/0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD) | Amount0: 151319316193.83 |
| 20127530 | 2024-06-19 18:19:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Value: 7100000.00 |
| 20127530 | 2024-06-19 18:19:23 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Amount0: 562499144609.14 |
| 20127671 | 2024-06-19 18:47:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x22F9dCF4...178C18](https://etherscan.io/address/0x22F9dCF4647084d6C31b2765F6910cd85C178C18) | Value: 364756.27 |
| 20127671 | 2024-06-19 18:47:35 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xE592427A...861564](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564) | Amount0: 28772575511.25 |
| 20127774 | 2024-06-19 19:08:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Value: 3500000.00 |
| 20127774 | 2024-06-19 19:08:23 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Amount0: 275467126206.26 |
| 20127797 | 2024-06-19 19:12:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x22F9dCF4...178C18](https://etherscan.io/address/0x22F9dCF4647084d6C31b2765F6910cd85C178C18) | Value: 1768874.32 |
| 20127797 | 2024-06-19 19:12:59 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xE592427A...861564](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564) | Amount0: 138794206945.92 |


## Risk Feature Breakdown

| Feature | Value | Weight | Contribution | Description |
|---------|-------|--------|-------------|-------------|
| Pool Concentration | 0.9752 | 0.15 | 0.1463 | Main pool holds 97.52% of total DEX liquidity. |
| Lp Concentration | 0.0000 | 0.15 | 0.0000 | Largest LP holds 0.00% of pool shares. |
| Withdrawal Severity | 1.0000 | 0.20 | 0.2000 | Liquidity removed is 100.00% of reference TVL. |
| Temporal Proximity | 0.4500 | 0.15 | 0.0675 | No incident block — 136 liquidity removals in window. |
| Role Sensitivity | 0.8000 | 0.15 | 0.1200 | Deployer is directly involved in pool(s). |
| Market Impact | 0.0000 | 0.15 | 0.0000 | No incident block — market impact requires a crash reference. |
| Combined Activity | 0.5000 | 0.05 | 0.0250 | Suspicious activity: 136 withdrawals. |
| **Raw Score** | | | **0.5588** | |

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
