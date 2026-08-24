# On-Chain Token Crash & Liquidity Risk Report

## Executive Summary

- **Token:** FTX Token ([0x50D1c977...55a4c9](https://etherscan.io/address/0x50D1c9771902476076eCFc8B2A83Ad6b9355a4c9))
- **Chain:** Ethereum (Chain ID: 1)
- **Analysis Window:** Block 15712530 to 15926369
- **Incident Block:** 15926371
- **Report Generated:** 2026-08-24 09:41:24 UTC

### Risk Score

| Metric | Value |
|--------|-------|
| **Final Risk Score** | **0.2758 / 1.00** |
| **Risk Level** | **LOW** |
| Evidence Confidence | 91.00% |
| Visual | `█████░░░░░░░░░░░░░░░` |
| Migration Adjustment | Liquidity migration detected — reducing risk by 0.30. |


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
| [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x56178a0d...345Bf9](https://etherscan.io/address/0x56178a0d5F301bAf6CF3e1Cd53d9863437345Bf9) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x98C3d318...8d6B8E](https://etherscan.io/address/0x98C3d3183C4b8A650614ad179A1a98be0a8d6B8E) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x7825dE55...3E1bf3](https://etherscan.io/address/0x7825dE5586E4d2FD04459091bbe783fa243E1bf3) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x00000000...91e2D4](https://etherscan.io/address/0x000000000dFDe7deaF24138722987c9a6991e2D4) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x9311d58f...d31E04](https://etherscan.io/address/0x9311d58f190d7190E7bc02927E81943C79d31E04) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xD249942f...790726](https://etherscan.io/address/0xD249942f6d417CbfdcB792B1229353B66c790726) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x38F93078...d88fcb](https://etherscan.io/address/0x38F9307839A8E82b071EA6Fcbef029814Ed88fcb) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x00000000...0f594e](https://etherscan.io/address/0x000000000035B5e5ad9019092C665357240f594e) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xaBd69D0f...fb81A9](https://etherscan.io/address/0xaBd69D0faC4b0851DAFe100979DF808Eb7fb81A9) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xF021F084...Db19E1](https://etherscan.io/address/0xF021F084477242fE6835c67234B4345de4Db19E1) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x5F0BeE21...4802C4](https://etherscan.io/address/0x5F0BeE213e5DC3F7b7Ca2A9d0b854468974802C4) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xE3bcA03b...61bFC9](https://etherscan.io/address/0xE3bcA03b772DdBe7FC806Da5Df6345c59961bFC9) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xA8BE07a5...d112FB](https://etherscan.io/address/0xA8BE07a56Ab39B22c7e58D88B2Ee401c34d112FB) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x6dD91Bda...7C38C0](https://etherscan.io/address/0x6dD91BdaB368282dc4Ea4f4beFc831b78a7C38C0) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xDEF171Fe...6FEe57](https://etherscan.io/address/0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57) | Frequent Token Sender | frequent_interactor | 50% |
| [0xeF6FA330...C18D4b](https://etherscan.io/address/0xeF6FA3307AF6ab6ddCc4826c4945041Dd5C18D4b) | Frequent Token Sender | frequent_interactor | 50% |
| [0xF2F400C1...B1b8a8](https://etherscan.io/address/0xF2F400C138F9fb900576263af0BC7fCde2B1b8a8) | Frequent Token Sender | frequent_interactor | 50% |
| [0xe8983D71...6f2a2e](https://etherscan.io/address/0xe8983D710315322CDF001c9C510da2e5676f2a2e) | Frequent Token Sender | frequent_interactor | 50% |
| [0x6264B7F0...54b799](https://etherscan.io/address/0x6264B7F05fACAdAf24b71a96E1Df3f46a654b799) | Frequent Token Sender | frequent_interactor | 50% |
| [0x699A8B3c...344073](https://etherscan.io/address/0x699A8B3cD08703359d78961dB51cabD872344073) | Frequent Token Sender | frequent_interactor | 50% |
| [0xE8c060F8...38A2e5](https://etherscan.io/address/0xE8c060F8052E07423f71D445277c61AC5138A2e5) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...000000](https://etherscan.io/address/0x0000000000000000000000000000000000000000) | Burn Address | burn | 100% |
| [0x00000000...00dead](https://etherscan.io/address/0x000000000000000000000000000000000000dead) | Burn Address | burn | 100% |
| [0x00000000...00dEaD](https://etherscan.io/address/0x000000000000000000000000000000000000dEaD) | Burn Address | burn | 100% |


## TVL & Price History

| Metric | Value |
|--------|-------|
| Total TVL (in token units) | 66916.3007 |
| Active Pools | 0 |
| Main Pool | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) |
| Main Pool Share | 60.28% |


## Liquidity Events

- **Liquidity Additions:** 94 events
- **Liquidity Removals:** 68 events

### Significant Liquidity Removals

| Block | Timestamp | Pool | Actor | Amount0 | Amount1 |
|-------|-----------|------|-------|---------|---------|
| 15922763 | 2022-11-08 03:56:11 UTC | [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | [0x7a250d56...F2488D](https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D) | 11.1221 | 130569561409.06 |
| 15922991 | 2022-11-08 04:41:59 UTC | [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | [0x7a250d56...F2488D](https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D) | 3.7082 | 43533583400.36 |
| 15835661 | 2022-10-26 23:54:47 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 1099.8484 | 638733260035.34 |
| 15907948 | 2022-11-06 02:19:35 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 657.6302 | 0 |
| 15909158 | 2022-11-06 06:22:23 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 23862.8321 | 0 |
| 15910253 | 2022-11-06 10:03:11 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 1191.2090 | 0 |
| 15913736 | 2022-11-06 21:42:23 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 169.9409 | 12771.2845 |
| 15916938 | 2022-11-07 08:25:35 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 675.6874 | 7.4200 |
| 15917023 | 2022-11-07 08:42:35 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 538.5899 | 12.5026 |
| 15917048 | 2022-11-07 08:47:35 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 27.1325 | 323782538346.69 |
| 15917501 | 2022-11-07 10:18:47 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 502.9026 | 1.0898 |
| 15917506 | 2022-11-07 10:19:47 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 205.4381 | 9.7049 |
| 15920429 | 2022-11-07 20:07:11 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 1142.4734 | 5.1787 |
| 15920529 | 2022-11-07 20:27:11 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 1349.8786 | 2.8709 |
| 15921516 | 2022-11-07 23:45:35 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 1043.1595 | 7.2364 |
| 15921803 | 2022-11-08 00:43:35 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 110.6902 | 610065784024.91 |
| 15922432 | 2022-11-08 02:49:35 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 1480.4905 | 0 |
| 15922432 | 2022-11-08 02:49:35 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 209.1185 | 0 |
| 15922439 | 2022-11-08 02:50:59 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 1329.3504 | 0 |
| 15922448 | 2022-11-08 02:52:47 UTC | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 453.5335 | 0 |


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
| Pre-Crash Withdrawals | 68 |
| Attributed Withdrawals | 51 |
| Total Removed (FTX Token) | 64453.75297358 |
| Pre-Event TVL | 66916.3007 |
| Withdrawal Severity | 96.32% of pre-event TVL |

### Removals by Pool

| Pool | Events | Removed (FTX Token) | Est. USD | % Pool TVL |
|------|--------|--------------|----------|------------|
| [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | 34 | 50461.29171568 | - | 125.11% |
| [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | 15 | 13977.63095611 | - | 59.92% |
| [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | 2 | 14.83030179 | - | 0.46% |


## Incident Timeline

| Metric | Value |
|--------|-------|
| Total Events | 7708 |
| Swaps | 3694 |
| Liquidity Events | 223 |
| Block Range | 15712530 → 15926369 |
| Time Range | 2022-10-09 19:08:59 UTC → 2022-11-08 15:59:47 UTC |

### Liquidity Migration Detected

The following migration candidates were found:
- From [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) (block 15913736) to [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) (block 15913736)
- From [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) (block 15923087) to [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) (block 15923087)
- From [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) (block 15925071) to [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) (block 15925073)
- From [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) (block 15926334) to [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) (block 15926338)
- From [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) (block 15734308) to [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) (block 15734308)

### Alternative Cause Check

- Large token distributions detected — possible airdrop or coordinated sell.

### Key Events by Block

| Block | Timestamp | Event | Pool | Actor | Detail |
|-------|-----------|-------|------|-------|--------|
| 15926275 | 2022-11-08 15:40:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Value: 125.7058 |
| 15926275 | 2022-11-08 15:40:59 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0x00000000...0f594e](https://etherscan.io/address/0x000000000035B5e5ad9019092C665357240f594e) | Amount0: 125.7058 |
| 15926275 | 2022-11-08 15:40:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Value: 817.8384 |
| 15926275 | 2022-11-08 15:40:59 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 817.8384 |
| 15926275 | 2022-11-08 15:40:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | Value: 143.7048 |
| 15926275 | 2022-11-08 15:40:59 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0x68b34658...65Fc45](https://etherscan.io/address/0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45) | Amount0: 143.7048 |
| 15926275 | 2022-11-08 15:40:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000000...0f594e](https://etherscan.io/address/0x000000000035B5e5ad9019092C665357240f594e) | Value: 125.7058 |
| 15926275 | 2022-11-08 15:40:59 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0x00000000...0f594e](https://etherscan.io/address/0x000000000035B5e5ad9019092C665357240f594e) | Amount0: 125.7058 |
| 15926275 | 2022-11-08 15:40:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x56178a0d...345Bf9](https://etherscan.io/address/0x56178a0d5F301bAf6CF3e1Cd53d9863437345Bf9) | Value: 460.8426 |
| 15926275 | 2022-11-08 15:40:59 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 460.8426 |
| 15926278 | 2022-11-08 15:41:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x7825dE55...3E1bf3](https://etherscan.io/address/0x7825dE5586E4d2FD04459091bbe783fa243E1bf3) | Value: 54.4833 |
| 15926278 | 2022-11-08 15:41:35 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0x0eae044f...d03000](https://etherscan.io/address/0x0eae044f00B0aF300500F090eA00027097d03000) | Amount0: 54.4833 |
| 15926279 | 2022-11-08 15:41:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x56178a0d...345Bf9](https://etherscan.io/address/0x56178a0d5F301bAf6CF3e1Cd53d9863437345Bf9) | Value: 232.5036 |
| 15926279 | 2022-11-08 15:41:47 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 232.5036 |
| 15926281 | 2022-11-08 15:42:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x9807ac1E...6D2663](https://etherscan.io/address/0x9807ac1Ec740B1b86FD947C94c7B9A9f326D2663) | Value: 289.3827 |
| 15926281 | 2022-11-08 15:42:11 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xDef1C0de...b25EfF](https://etherscan.io/address/0xDef1C0ded9bec7F1a1670819833240f027b25EfF) | Amount0: 289.3827 |
| 15926282 | 2022-11-08 15:42:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Value: 86.0730 |
| 15926282 | 2022-11-08 15:42:23 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0x0eae044f...d03000](https://etherscan.io/address/0x0eae044f00B0aF300500F090eA00027097d03000) | Amount0: 86.0730 |
| 15926282 | 2022-11-08 15:42:23 UTC | SWAP (Swap) | [0x9D2713fa...Da2A71](https://etherscan.io/address/0x9D2713fa2f387eD1284a4176E7841253B4Da2A71) | [0x0eae044f...d03000](https://etherscan.io/address/0x0eae044f00B0aF300500F090eA00027097d03000) | Amount0: 86.0729 |
| 15926282 | 2022-11-08 15:42:23 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Value: 81.2895 |
| 15926282 | 2022-11-08 15:42:23 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 81.2895 |
| 15926284 | 2022-11-08 15:42:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | Value: 254.0559 |
| 15926284 | 2022-11-08 15:42:47 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xeF6FA330...C18D4b](https://etherscan.io/address/0xeF6FA3307AF6ab6ddCc4826c4945041Dd5C18D4b) | Amount0: 254.0559 |
| 15926285 | 2022-11-08 15:42:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x56178a0d...345Bf9](https://etherscan.io/address/0x56178a0d5F301bAf6CF3e1Cd53d9863437345Bf9) | Value: 201.3626 |
| 15926285 | 2022-11-08 15:42:59 UTC | SWAP (Swap) | [0xb404057E...23E56b](https://etherscan.io/address/0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b) | [0xA69babEF...56e78C](https://etherscan.io/address/0xA69babEF1cA67A37Ffaf7a485DfFF3382056e78C) | Amount0: 201.3626 |
| 15926288 | 2022-11-08 15:43:35 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xF021F084...Db19E1](https://etherscan.io/address/0xF021F084477242fE6835c67234B4345de4Db19E1) | Value: 15.5545 |
| 15926288 | 2022-11-08 15:43:35 UTC | SWAP (Swap) | [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | [0xF021F084...Db19E1](https://etherscan.io/address/0xF021F084477242fE6835c67234B4345de4Db19E1) | Amount0: 15.5545 |
| 15926296 | 2022-11-08 15:45:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xEAC9eca0...c158e7](https://etherscan.io/address/0xEAC9eca0644E684c53D44403f08485274Bc158e7) | Value: 2.8707 |
| 15926296 | 2022-11-08 15:45:11 UTC | SWAP (Swap) | [0xF04543fB...Ae0F5A](https://etherscan.io/address/0xF04543fBF20DAEE9B0357db966428EF2A4Ae0F5A) | [0xDef1C0de...b25EfF](https://etherscan.io/address/0xDef1C0ded9bec7F1a1670819833240f027b25EfF) | Amount0: 2.8707 |
| 15926299 | 2022-11-08 15:45:47 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x56178a0d...345Bf9](https://etherscan.io/address/0x56178a0d5F301bAf6CF3e1Cd53d9863437345Bf9) | Value: 159.9598 |


## Risk Feature Breakdown

| Feature | Value | Weight | Contribution | Description |
|---------|-------|--------|-------------|-------------|
| Pool Concentration | 0.6028 | 0.15 | 0.0904 | Main pool holds 60.28% of total DEX liquidity. |
| Lp Concentration | 0.0000 | 0.15 | 0.0000 | Largest LP holds 0.00% of pool shares. |
| Withdrawal Severity | 0.9632 | 0.20 | 0.1926 | Liquidity removed is 96.32% of reference TVL. |
| Temporal Proximity | 1.0000 | 0.15 | 0.1500 | Withdrawal within 1 hour of crash |
| Role Sensitivity | 0.8000 | 0.15 | 0.1200 | Deployer is directly involved in pool(s). |
| Market Impact | 0.0000 | 0.15 | 0.0000 | No significant price change detected. |
| Combined Activity | 1.0000 | 0.05 | 0.0500 | Suspicious activity: 68 withdrawals and large sells detected. |
| **Raw Score** | | | **0.6030** | |

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

