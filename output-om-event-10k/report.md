# On-Chain Token Crash & Liquidity Risk Report

## Executive Summary

- **Token:** OM ([0x3593D125...60c95d](https://etherscan.io/address/0x3593D125a4f7849a1B059E64F4517A86Dd60c95d))
- **Chain:** Ethereum (Chain ID: 1)
- **Analysis Window:** Block 22251875 to 22261846
- **Incident Block:** 22261846
- **Report Generated:** 2026-09-01 07:13:37 UTC

### Risk Score

| Metric | Value |
|--------|-------|
| **Final Risk Score** | **0.3346 / 1.00** |
| **Risk Level** | **LOW** |
| Evidence Confidence | 91.00% |
| Visual | `██████░░░░░░░░░░░░░░` |


## Token Profile

| Property | Value |
|----------|-------|
| Address | [0x3593D125...60c95d](https://etherscan.io/address/0x3593D125a4f7849a1B059E64F4517A86Dd60c95d) |
| Symbol | OM |
| Name | MANTRA DAO |
| Decimals | 18 (onchain) |
| Total Supply | 888888888.0000 |
| Is Contract | True |
| Proxy Address | None |
| Implementation | None |
| Behavior Flags | minting |


## Pool Summary

**7** verified pool(s), **0** unverified candidate(s).

| Pool Address | Protocol | Version | Token0 | Token1 | Fee | Confidence |
|-------------|----------|---------|--------|--------|-----|------------|
| [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | uniswap | v2 | 0x3593D125... | 0xC02aaA39... | N/A | 100.00% |
| [0x65c3C7cB...B28DA6](https://etherscan.io/address/0x65c3C7cB15473f6F86c7528D52237E5eA7B28DA6) | uniswap | v2 | 0x3593D125... | 0xdAC17F95... | N/A | 100.00% |
| [0x841D7892...95B807](https://etherscan.io/address/0x841D78928792729bb745f8DB37a10b335595B807) | uniswap | v3 | 0x3593D125... | 0xC02aaA39... | 500 | 100.00% |
| [0x9C289f2B...Ea45d5](https://etherscan.io/address/0x9C289f2B496D7756f15378Fab71B5206d7Ea45d5) | uniswap | v3 | 0x3593D125... | 0xC02aaA39... | 3000 | 100.00% |
| [0x8646047a...308C72](https://etherscan.io/address/0x8646047a7Ea7fef0836a81e797FFAb816c308C72) | uniswap | v3 | 0x3593D125... | 0xC02aaA39... | 10000 | 100.00% |
| [0x97e0fD7e...88ABBD](https://etherscan.io/address/0x97e0fD7e397BFD81f209ed08e63E2cF89288ABBD) | uniswap | v3 | 0x3593D125... | 0xA0b86991... | 3000 | 100.00% |
| [0x179F3dB3...C505be](https://etherscan.io/address/0x179F3dB346851d1A9f4Ff7EbA57eABb91CC505be) | uniswap | v3 | 0x3593D125... | 0xdAC17F95... | 10000 | 100.00% |


## Related Addresses

| Address | Label | Category | Confidence |
|---------|-------|----------|------------|
| [0x5C69bEe7...c5aA6f](https://etherscan.io/address/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f) | Factory (uniswap)_v2 | protocol_deployment | 100% |
| [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | Uniswap V2 Pool | pool | 100% |
| [0x7a250d56...F2488D](https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D) | Router (uniswap_v2) | router | 100% |
| [0x65c3C7cB...B28DA6](https://etherscan.io/address/0x65c3C7cB15473f6F86c7528D52237E5eA7B28DA6) | Uniswap V2 Pool | pool | 100% |
| [0x1F98431c...31F984](https://etherscan.io/address/0x1F98431c8aD98523631AE4a59f267346ea31F984) | Factory (uniswap)_v3 | protocol_deployment | 100% |
| [0x841D7892...95B807](https://etherscan.io/address/0x841D78928792729bb745f8DB37a10b335595B807) | Uniswap V3 Pool | pool | 100% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | PositionManager (uniswap_v3) | position_manager | 100% |
| [0xE592427A...861564](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564) | Router (uniswap_v3) | router | 100% |
| [0x9C289f2B...Ea45d5](https://etherscan.io/address/0x9C289f2B496D7756f15378Fab71B5206d7Ea45d5) | Uniswap V3 Pool | pool | 100% |
| [0x8646047a...308C72](https://etherscan.io/address/0x8646047a7Ea7fef0836a81e797FFAb816c308C72) | Uniswap V3 Pool | pool | 100% |
| [0x97e0fD7e...88ABBD](https://etherscan.io/address/0x97e0fD7e397BFD81f209ed08e63E2cF89288ABBD) | Uniswap V3 Pool | pool | 100% |
| [0x179F3dB3...C505be](https://etherscan.io/address/0x179F3dB346851d1A9f4Ff7EbA57eABb91CC505be) | Uniswap V3 Pool | pool | 100% |
| [0xFa0e08b7...2da295](https://etherscan.io/address/0xFa0e08b7e80E6e7eeCAd9800Bc32eF19132da295) | Deployer | token_creator | 100% |
| [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x8646047a...308C72](https://etherscan.io/address/0x8646047a7Ea7fef0836a81e797FFAb816c308C72) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xfBd4cdB4...794C37](https://etherscan.io/address/0xfBd4cdB413E45a52E2C8312f670e9cE67E794C37) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xe0427A92...147e50](https://etherscan.io/address/0xe0427A927929aBD3cFB017B7844550d4Bf147e50) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xff62388c...A0cF8F](https://etherscan.io/address/0xff62388c39F4A5C4D58B0E5B7f07438E59A0cF8F) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x66a9893c...dBA8Af](https://etherscan.io/address/0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x1f2F10D1...6Df387](https://etherscan.io/address/0x1f2F10D1C40777AE1Da742455c65828FF36Df387) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x9C289f2B...Ea45d5](https://etherscan.io/address/0x9C289f2B496D7756f15378Fab71B5206d7Ea45d5) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...842A65](https://etherscan.io/address/0x111111125421cA6dc452d289314280a0f8842A65) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xDEF171Fe...6FEe57](https://etherscan.io/address/0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x11111112...960582](https://etherscan.io/address/0x1111111254EEB25477B68fb85Ed929f73A960582) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x00000000...E08A90](https://etherscan.io/address/0x000000000004444c5dc75cB358380D2e3dE08A90) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x5141B82f...40a190](https://etherscan.io/address/0x5141B82f5fFDa4c6fE1E372978F1C5427640a190) | Frequent Token Sender | frequent_interactor | 50% |
| [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Frequent Token Sender | frequent_interactor | 50% |
| [0xEff6cb8b...1aA167](https://etherscan.io/address/0xEff6cb8b614999d130E537751Ee99724D01aA167) | Frequent Token Sender | frequent_interactor | 50% |
| [0x5b0F6aC7...2274C8](https://etherscan.io/address/0x5b0F6aC7228015b2EC2Ac5bB8DDEc86AEa2274C8) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...00dead](https://etherscan.io/address/0x000000000000000000000000000000000000dead) | Burn Address | burn | 100% |
| [0x00000000...000000](https://etherscan.io/address/0x0000000000000000000000000000000000000000) | Burn Address | burn | 100% |
| [0x00000000...00dEaD](https://etherscan.io/address/0x000000000000000000000000000000000000dEaD) | Burn Address | burn | 100% |


## TVL & Price History

| Metric | Value |
|--------|-------|
| Total TVL (in token units) | 757369.1639 |
| Active Pools | 0 |
| Main Pool | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) |
| Main Pool Share | 98.38% |


## Liquidity Events

- **Liquidity Additions:** 0 events
- **Liquidity Removals:** 3 events

### Significant Liquidity Removals

| Block | Timestamp | Pool | Actor | Amount0 | Amount1 |
|-------|-----------|------|-------|---------|---------|
| 22255043 | 2025-04-12 19:42:59 UTC | [0x8646047a...308C72](https://etherscan.io/address/0x8646047a7Ea7fef0836a81e797FFAb816c308C72) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 691.4948 | 2.6573 |


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
| Pre-Crash Withdrawals | 3 |
| Attributed Withdrawals | 1 |
| Total Removed (OM) | 691.49484411 |
| Pre-Event TVL | 757369.1639 |
| Withdrawal Severity | 0.09% of pre-event TVL |

### Removals by Pool

| Pool | Events | Removed (OM) | Est. USD | % Pool TVL |
|------|--------|--------------|----------|------------|
| [0x8646047a...308C72](https://etherscan.io/address/0x8646047a7Ea7fef0836a81e797FFAb816c308C72) | 1 | 691.49484411 | - | 5.63% |


## Incident Timeline

| Metric | Value |
|--------|-------|
| Total Events | 1586 |
| Swaps | 789 |
| Liquidity Events | 6 |
| Block Range | 22251875 → 22261846 |
| Time Range | 2025-04-12 09:06:35 UTC → 2025-04-13 18:28:11 UTC |

### Alternative Cause Check

- Large token distributions detected — possible airdrop or coordinated sell.

### Key Events by Block

| Block | Timestamp | Event | Pool | Actor | Detail |
|-------|-----------|-------|------|-------|--------|
| 22261754 | 2025-04-13 18:09:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | Value: 119.1136 |
| 22261754 | 2025-04-13 18:09:47 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0x66a9893c...dBA8Af](https://etherscan.io/address/0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af) | Amount0: -119113583360118030538 |
| 22261760 | 2025-04-13 18:10:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Value: 315.1282 |
| 22261760 | 2025-04-13 18:10:59 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Amount0: 315.1282 |
| 22261760 | 2025-04-13 18:10:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Value: 245.8533 |
| 22261760 | 2025-04-13 18:10:59 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 245.8533 |
| 22261761 | 2025-04-13 18:11:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Value: 315.4540 |
| 22261761 | 2025-04-13 18:11:11 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Amount0: 315.4540 |
| 22261763 | 2025-04-13 18:11:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | Value: 14.2522 |
| 22261763 | 2025-04-13 18:11:35 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0x1f2F10D1...6Df387](https://etherscan.io/address/0x1f2F10D1C40777AE1Da742455c65828FF36Df387) | Amount0: -14252199491116466176 |
| 22261763 | 2025-04-13 18:11:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x1f2F10D1...6Df387](https://etherscan.io/address/0x1f2F10D1C40777AE1Da742455c65828FF36Df387) | Value: 1.0960 |
| 22261763 | 2025-04-13 18:11:35 UTC | SWAP (Swap) | [0x9C289f2B...Ea45d5](https://etherscan.io/address/0x9C289f2B496D7756f15378Fab71B5206d7Ea45d5) | [0x1f2F10D1...6Df387](https://etherscan.io/address/0x1f2F10D1C40777AE1Da742455c65828FF36Df387) | Amount0: 1.0960 |
| 22261764 | 2025-04-13 18:11:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Value: 316.2530 |
| 22261764 | 2025-04-13 18:11:47 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Amount0: 316.2530 |
| 22261765 | 2025-04-13 18:11:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Value: 204.1764 |
| 22261765 | 2025-04-13 18:11:59 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 204.1764 |
| 22261766 | 2025-04-13 18:12:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Value: 317.2267 |
| 22261766 | 2025-04-13 18:12:11 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Amount0: 317.2267 |
| 22261767 | 2025-04-13 18:12:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Value: 317.7595 |
| 22261767 | 2025-04-13 18:12:23 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0xfbEedCFe...768737](https://etherscan.io/address/0xfbEedCFe378866DaB6abbaFd8B2986F5C1768737) | Amount0: 317.7595 |
| 22261767 | 2025-04-13 18:12:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xCD16Bb51...3A62BB](https://etherscan.io/address/0xCD16Bb511417FE6cA065C31E982A4120d43A62BB) | Value: 118.8158 |
| 22261767 | 2025-04-13 18:12:23 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0x66a9893c...dBA8Af](https://etherscan.io/address/0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af) | Amount0: 118.8158 |
| 22261767 | 2025-04-13 18:12:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | Value: 5.9116 |
| 22261767 | 2025-04-13 18:12:23 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0x0eae044f...d03000](https://etherscan.io/address/0x0eae044f00B0aF300500F090eA00027097d03000) | Amount0: -5911583879844515253 |
| 22261769 | 2025-04-13 18:12:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Value: 664.1414 |
| 22261769 | 2025-04-13 18:12:47 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0x55877bD7...7ef121](https://etherscan.io/address/0x55877bD7F2EE37BDe55cA4B271A3631f3A7ef121) | Amount0: 664.1414 |
| 22261769 | 2025-04-13 18:12:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | Value: 5.9362 |
| 22261769 | 2025-04-13 18:12:47 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0x06CFf708...d2f5ef](https://etherscan.io/address/0x06CFf7088619C7178F5e14f0B119458d08d2f5ef) | Amount0: -5936200433824197046 |
| 22261769 | 2025-04-13 18:12:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | Value: 17.8074 |
| 22261769 | 2025-04-13 18:12:47 UTC | SWAP (Swap) | [0xe46935aE...845370](https://etherscan.io/address/0xe46935aE80E05cdEbD4a4008B6ccaA36d2845370) | [0x06CFf708...d2f5ef](https://etherscan.io/address/0x06CFf7088619C7178F5e14f0B119458d08d2f5ef) | Amount0: -17807430942452621442 |


## Risk Feature Breakdown

| Feature | Value | Weight | Contribution | Description |
|---------|-------|--------|-------------|-------------|
| Pool Concentration | 0.9838 | 0.15 | 0.1476 | Main pool holds 98.38% of total DEX liquidity. |
| Lp Concentration | 0.0000 | 0.15 | 0.0000 | Largest LP holds 0.00% of pool shares. |
| Withdrawal Severity | 0.0009 | 0.20 | 0.0002 | Liquidity removed is 0.09% of reference TVL. |
| Temporal Proximity | 0.5000 | 0.15 | 0.0750 | Withdrawal within 24 hours of crash |
| Role Sensitivity | 0.8000 | 0.15 | 0.1200 | Deployer is directly involved in pool(s). |
| Market Impact | 0.0000 | 0.15 | 0.0000 | No significant price change detected. |
| Combined Activity | 0.5000 | 0.05 | 0.0250 | Suspicious activity: 3 withdrawals. |
| **Raw Score** | | | **0.3678** | |

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
