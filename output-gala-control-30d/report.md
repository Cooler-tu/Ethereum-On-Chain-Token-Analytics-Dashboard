# On-Chain Token Crash & Liquidity Risk Report

## Executive Summary

- **Token:** GALA ([0xd1d2Eb1B...C87cae](https://etherscan.io/address/0xd1d2Eb1B1e90B638588728b4130137D262C87cae))
- **Chain:** Ethereum (Chain ID: 1)
- **Analysis Window:** Block 19698766 to 19913229
- **Incident Block:** Not specified
- **Report Generated:** 2026-08-29 09:12:05 UTC

### Risk Score

| Metric | Value |
|--------|-------|
| **Final Risk Score** | **0.2368 / 1.00** |
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
| [0x3fC91A3a...2b7FAD](https://etherscan.io/address/0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xf5213a6a...1A9900](https://etherscan.io/address/0xf5213a6a2f0890321712520b8048D9886c1A9900) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x72e364F2...d634D7](https://etherscan.io/address/0x72e364F2ABdC788b7E918bc238B21f109Cd634D7) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x22F9dCF4...178C18](https://etherscan.io/address/0x22F9dCF4647084d6C31b2765F6910cd85C178C18) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xa7Ca2C86...0Db22A](https://etherscan.io/address/0xa7Ca2C8673bcFA5a26d8ceeC2887f2CC2b0Db22A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...43097d](https://etherscan.io/address/0x1111111254fb6c44bAC0beD2854e76F90643097d) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x98C3d318...8d6B8E](https://etherscan.io/address/0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...842A65](https://etherscan.io/address/0x111111125421cA6dc452d289314280a0f8842A65) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x6F1cDbBb...AB6168](https://etherscan.io/address/0x6F1cDbBb4d53d226CF4B917bF768B94acbAB6168) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xc61AA086...965a1E](https://etherscan.io/address/0xc61AA0867ef045E343A5FB427259e0e863965a1E) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x0055Ae46...007200](https://etherscan.io/address/0x0055Ae46f700BcC53B1b00483d64000d47007200) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x13307b88...7a577b](https://etherscan.io/address/0x13307b8854a95946b54A904100AFd0767a7a577b) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xE37e799D...57BD09](https://etherscan.io/address/0xE37e799D5077682FA0a244D46E5649F71457BD09) | Frequent Token Sender | frequent_interactor | 50% |
| [0xf081470f...DcdD67](https://etherscan.io/address/0xf081470f5C6FBCCF48cC4e5B82Dd926409DcdD67) | Frequent Token Sender | frequent_interactor | 50% |
| [0x9008D19f...60ab41](https://etherscan.io/address/0x9008D19f58AAbD9eD0D60971565AA8510560ab41) | Frequent Token Sender | frequent_interactor | 50% |
| [0xe43ca1De...1A59F5](https://etherscan.io/address/0xe43ca1Dee3F0fc1e2df73A0745674545F11A59F5) | Frequent Token Sender | frequent_interactor | 50% |
| [0xCf637D24...C6f885](https://etherscan.io/address/0xCf637D2435293eA11Bf768300581107f72C6f885) | Frequent Token Sender | frequent_interactor | 50% |
| [0x713aEA8F...26d845](https://etherscan.io/address/0x713aEA8F006dba6b0Ba8d766333B134A9E26d845) | Frequent Token Sender | frequent_interactor | 50% |
| [0x663DC15D...83C251](https://etherscan.io/address/0x663DC15D3C1aC63ff12E45Ab68FeA3F0a883C251) | Frequent Token Sender | frequent_interactor | 50% |
| [0xad3b67BC...4A968f](https://etherscan.io/address/0xad3b67BCA8935Cb510C8D18bD45F0b94F54A968f) | Frequent Token Sender | frequent_interactor | 50% |
| [0xa9C0cdEd...9BC59a](https://etherscan.io/address/0xa9C0cdEd336699547aaC4f9De5A11Ada979BC59a) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...00dEaD](https://etherscan.io/address/0x000000000000000000000000000000000000dEaD) | Burn Address | burn | 100% |
| [0x00000000...00dead](https://etherscan.io/address/0x000000000000000000000000000000000000dead) | Burn Address | burn | 100% |
| [0x00000000...000000](https://etherscan.io/address/0x0000000000000000000000000000000000000000) | Burn Address | burn | 100% |


## TVL & Price History

| Metric | Value |
|--------|-------|
| Total TVL (in token units) | 8558365738.19 |
| Active Pools | 0 |
| Main Pool | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) |
| Main Pool Share | 98.47% |


## Liquidity Events

- **Liquidity Additions:** 72 events
- **Liquidity Removals:** 92 events

### Significant Liquidity Removals

| Block | Timestamp | Pool | Actor | Amount0 | Amount1 |
|-------|-----------|------|-------|---------|---------|
| 19700608 | 2024-04-21 01:49:11 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 2.1026 | 10339361.21 |
| 19702477 | 2024-04-21 08:05:59 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | 297.6009 | 441414760.30 |
| 19707930 | 2024-04-22 02:22:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | 197.8589 | 417786746.22 |
| 19708421 | 2024-04-22 04:01:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | 2035.2071 | 201640539.57 |
| 19712757 | 2024-04-22 18:34:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | 3565.9926 | 481005487.89 |
| 19717352 | 2024-04-23 09:59:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | 3.1645 | 464711207.14 |
| 19720247 | 2024-04-23 19:41:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 8.3229 | 0 |
| 19733540 | 2024-04-25 16:21:47 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | 59.2623 | 424354198.56 |
| 19738250 | 2024-04-26 08:08:59 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 1.3717 | 19476566.42 |
| 19742301 | 2024-04-26 21:48:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 1.1989 | 20648719.72 |
| 19743366 | 2024-04-27 01:22:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x000000d4...3A51d3](https://etherscan.io/address/0x000000d40B595B94918a28b27d1e2C66F43A51d3) | 126.7866 | 7777925.16 |
| 19749001 | 2024-04-27 20:18:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | 10.3198 | 377792413.29 |
| 19755523 | 2024-04-28 18:11:59 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 16.8548 | 10623043.45 |
| 19765239 | 2024-04-30 02:48:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 93.5942 | 152959501.88 |
| 19765489 | 2024-04-30 03:38:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | 213.8266 | 443153652.37 |
| 19767186 | 2024-04-30 09:18:47 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 1.4478 | 10397865.10 |
| 19771098 | 2024-04-30 22:27:11 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 54.9419 | 38253468.51 |
| 19776090 | 2024-05-01 15:11:23 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 6.9779 | 28703776.60 |
| 19783582 | 2024-05-02 16:18:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x6b75d8AF...009A80](https://etherscan.io/address/0x6b75d8AF000000e20B7a7DDf000Ba900b4009A80) | 1.6431 | 17172774.97 |
| 19794918 | 2024-05-04 06:21:35 UTC | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | 6127.0650 | 14772854.51 |


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
| Pre-Crash Withdrawals | 92 |
| Attributed Withdrawals | 63 |
| Total Removed (GALA) | 196789698.81034476 |
| Pre-Event TVL | 8558365738.19 |
| Withdrawal Severity | 100.00% of pre-event TVL |

### Removals by Pool

| Pool | Events | Removed (GALA) | Est. USD | % Pool TVL |
|------|--------|--------------|----------|------------|
| [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | 62 | 196784485.9824035 | - | 233.51% |
| [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | 1 | 5212.8279413 | - | 0.40% |


## Incident Timeline

| Metric | Value |
|--------|-------|
| Total Events | 12129 |
| Swaps | 5879 |
| Liquidity Events | 252 |
| Block Range | 19698766 → 19913229 |
| Time Range | 2024-04-20 19:39:11 UTC → 2024-05-20 19:31:35 UTC |

### Liquidity Migration Detected

The following migration candidates were found:
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19700608) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19700608)
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19702477) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19702477)
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19707930) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19707930)
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19708421) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19708421)
- From [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19712757) to [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) (block 19712757)

### Alternative Cause Check

- Large token distributions detected — possible airdrop or coordinated sell.

### Key Events by Block

| Block | Timestamp | Event | Pool | Actor | Detail |
|-------|-----------|-------|------|-------|--------|
| 19913163 | 2024-05-20 19:18:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Value: 10409797.47 |
| 19913163 | 2024-05-20 19:18:11 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 1.5324 |
| 19913181 | 2024-05-20 19:21:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Value: 10699156.33 |
| 19913181 | 2024-05-20 19:21:47 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Amount0: 1.5722 |
| 19913186 | 2024-05-20 19:22:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Value: 17595883.98 |
| 19913186 | 2024-05-20 19:22:59 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Amount0: 2.5794 |
| 19913188 | 2024-05-20 19:23:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Value: 16560113.45 |
| 19913188 | 2024-05-20 19:23:23 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Amount0: 2.4221 |
| 19913190 | 2024-05-20 19:23:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Value: 24788150.03 |
| 19913190 | 2024-05-20 19:23:47 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Amount0: 3.6172 |
| 19913192 | 2024-05-20 19:24:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xc61AA086...965a1E](https://etherscan.io/address/0xc61AA0867ef045E343A5FB427259e0e863965a1E) | Value: 35822221.89 |
| 19913192 | 2024-05-20 19:24:11 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x2f1d7986...3c0638](https://etherscan.io/address/0x2f1d79860cf6ea3F4B3b734153B52815773c0638) | Amount0: 5.2100 |
| 19913194 | 2024-05-20 19:24:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Value: 58641406.61 |
| 19913194 | 2024-05-20 19:24:35 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Amount0: 8.4847 |
| 19913196 | 2024-05-20 19:24:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Value: 33019797.97 |
| 19913196 | 2024-05-20 19:24:59 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 4.7536 |
| 19913199 | 2024-05-20 19:25:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Value: 37374725.62 |
| 19913199 | 2024-05-20 19:25:35 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Amount0: 5.3599 |
| 19913203 | 2024-05-20 19:26:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Value: 55588547.96 |
| 19913203 | 2024-05-20 19:26:23 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Amount0: 7.9316 |
| 19913221 | 2024-05-20 19:29:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Value: 36681730.44 |
| 19913221 | 2024-05-20 19:29:59 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x51C72848...502a7F](https://etherscan.io/address/0x51C72848c68a965f66FA7a88855F9f7784502a7F) | Amount0: 5.2077 |
| 19913223 | 2024-05-20 19:30:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Value: 43940282.26 |
| 19913223 | 2024-05-20 19:30:23 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 6.2110 |
| 19913226 | 2024-05-20 19:30:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xc61AA086...965a1E](https://etherscan.io/address/0xc61AA0867ef045E343A5FB427259e0e863965a1E) | Value: 40004588.83 |
| 19913226 | 2024-05-20 19:30:59 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x2f1d7986...3c0638](https://etherscan.io/address/0x2f1d79860cf6ea3F4B3b734153B52815773c0638) | Amount0: 5.6290 |
| 19913227 | 2024-05-20 19:31:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xc61AA086...965a1E](https://etherscan.io/address/0xc61AA0867ef045E343A5FB427259e0e863965a1E) | Value: 37732846.99 |
| 19913227 | 2024-05-20 19:31:11 UTC | SWAP (Swap) | [0x465E56cD...0C3719](https://etherscan.io/address/0x465E56cD21ad47d4d4790F17de5E0458F20C3719) | [0x2f1d7986...3c0638](https://etherscan.io/address/0x2f1d79860cf6ea3F4B3b734153B52815773c0638) | Amount0: 5.2870 |
| 19913229 | 2024-05-20 19:31:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Value: 2200000.00 |
| 19913229 | 2024-05-20 19:31:35 UTC | SWAP (Swap) | [0x72B1410d...0C579A](https://etherscan.io/address/0x72B1410df9d22D5a3416066663fcc36b460C579A) | [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Amount0: -318156063967148401 |


## Risk Feature Breakdown

| Feature | Value | Weight | Contribution | Description |
|---------|-------|--------|-------------|-------------|
| Pool Concentration | 0.9847 | 0.15 | 0.1477 | Main pool holds 98.47% of total DEX liquidity. |
| Lp Concentration | 0.0000 | 0.15 | 0.0000 | Largest LP holds 0.00% of pool shares. |
| Withdrawal Severity | 1.0000 | 0.20 | 0.2000 | Liquidity removed is 100.00% of reference TVL. |
| Temporal Proximity | 0.4500 | 0.15 | 0.0675 | No incident block — 92 liquidity removals in window. |
| Role Sensitivity | 0.8000 | 0.15 | 0.1200 | Deployer is directly involved in pool(s). |
| Market Impact | 0.0000 | 0.15 | 0.0000 | No incident block — market impact requires a crash reference. |
| Combined Activity | 0.5000 | 0.05 | 0.0250 | Suspicious activity: 92 withdrawals. |
| **Raw Score** | | | **0.5602** | |

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
