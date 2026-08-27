# Targeted V3 position trace

- Transactions traced: **18**
- Pool Mint/Burn events decoded: **18**
- Exact Position Manager amount matches: **17/18**
- Unique NFT tokenIds: **14**
- Unique transaction senders: **10**
- Range shape at hour close: target-only **2**, two-sided **16**, WETH-only **0**
- Same-NFT opposite-action pairs inside the selected transaction set: **1**

| Case | Rank | Event | NFT | Tx sender | Owner at block | Ticks | Range shape | Tx |
|---|---:|---|---:|---|---|---:|---|---|
| FTT | 1 | Burn | 346040 | `0x8a039340b3caa9249ed5201c197a0c4c4c4efd25` | `0x8a039340b3caa9249ed5201c197a0c4c4c4efd25` | -42240→-40680 | target_only_below_range | `0x170fe56b9f422442d70e74d282c36aec335d99886ac1de3149234ca8ecb28d05` |
| FTT | 1 | Mint | 354342 | `0x74f53ed1175715d126c0c95d3b1b20f67c8a1273` | `0x74f53ed1175715d126c0c95d3b1b20f67c8a1273` | -42240→-42180 | target_only_below_range | `0xdb02be35e4708f15f671d15367fed22fa3922fb658cdaf96e19f796d4e439010` |
| FTT | 2 | Burn | 355173 | `0x01f0831120ab81f91109e099afb551a091c4c05a` | `0x01f0831120ab81f91109e099afb551a091c4c05a` | -48800→-35800 | two_sided_in_range | `0xadf1f2f6fa4943c449e19f4efe683ec34f18df53483b02086616f395c3b2d9bf` |
| FTT | 2 | Mint | 355173 | `0x01f0831120ab81f91109e099afb551a091c4c05a` | `0x01f0831120ab81f91109e099afb551a091c4c05a` | -48800→-35800 | two_sided_in_range | `0xead43ccd6fb8abea815993bca9091529d9f441c3dfdac758c0e7676817f136ad` |
| FTT | 2 | Mint | 355198 | `0x053ab16a247321e312f3a8a2a0a8abda48707241` | `0x053ab16a247321e312f3a8a2a0a8abda48707241` | -46500→-39720 | two_sided_in_range | `0xb2eacc929eebf127f8fca11cf79d6dce5d42382c47adf79d2c9d6ac71ed866b0` |
| FTT | 2 | Mint | 355187 | `0x01f0831120ab81f91109e099afb551a091c4c05a` | `0x01f0831120ab81f91109e099afb551a091c4c05a` | -48120→-37020 | two_sided_in_range | `0xc39a3dd49014b8eb1cd77faf7e70a7cdccb5587943d578c7b9ed2e2ced080d81` |
| FTT | 3 | Mint | 349801 | `0x8eab1448f99e102067b8d370b7f413d0f14e4b7d` | `0x8eab1448f99e102067b8d370b7f413d0f14e4b7d` | -43800→-37800 | two_sided_in_range | `0x4e207809838d19ff307daba753b5c624f8aea0c26386ea4a2805284aded4a6b0` |
| FTT | 4 | Mint | 355207 | `0x053ab16a247321e312f3a8a2a0a8abda48707241` | `0x053ab16a247321e312f3a8a2a0a8abda48707241` | -47000→-39800 | two_sided_in_range | `0xc004aa664131f3617ce39df0acce52fa5badaba72111de1e1da9b2734f336b87` |
| FTT | 4 | Mint | 355210 | `0x6dd91bdab368282dc4ea4f4befc831b78a7c38c0` | `0x6dd91bdab368282dc4ea4f4befc831b78a7c38c0` | -43320→-42300 | two_sided_in_range | `0x6d5fc2365ec804a5d89347ce9443bd08821888253709cd5fd2906eafb64b6b4d` |
| FTT | 4 | Mint | 355210 | `0x6dd91bdab368282dc4ea4f4befc831b78a7c38c0` | `0x6dd91bdab368282dc4ea4f4befc831b78a7c38c0` | -43320→-42300 | two_sided_in_range | `0xa47ba05463ee4cbfaea646ab8c244e4bf3175fa7ab8e31ebfb63a1009e9923a6` |
| FTT | 4 | Mint | 355210 | `0x6dd91bdab368282dc4ea4f4befc831b78a7c38c0` | `0x6dd91bdab368282dc4ea4f4befc831b78a7c38c0` | -43320→-42300 | two_sided_in_range | `0xe593748370b837334e0059ccc3d0fd98634af12530ba86862e5ae1d9da9bf728` |
| FTT | 5 | Mint | 344744 | `0x8a039340b3caa9249ed5201c197a0c4c4c4efd25` | `0x8a039340b3caa9249ed5201c197a0c4c4c4efd25` | -41400→-40600 | two_sided_in_range | `0x99407380b491f9a59551fdf6a9a936aa46380b7d24792fa8b263e3d68b1f4c15` |
| CEL | 1 | Mint | 239116 | `0x376731891c47fab75ccf690ad9afc6d3fa4a46c8` | `0x376731891c47fab75ccf690ad9afc6d3fa4a46c8` | 243780→245820 | two_sided_in_range | `0x792c5c3a96a88086d19b17c426bd8160382357f1ffa3ba78ff31ba63f4d02f11` |
| CEL | 2 | Mint | 241973 | `0x48f773b3094d10862c9c4dad5ef37ae89244ce87` | `0x48f773b3094d10862c9c4dad5ef37ae89244ce87` | 243720→245400 | two_sided_in_range | `0x8db65900999c773532de3745ca0cc82929ac9602d4132097c20eaa6837f2bb16` |
| CEL | 3 | Mint | 245751 | `0x7328abfa5a662e583eef0ed5836a2469202467a2` | `0x7328abfa5a662e583eef0ed5836a2469202467a2` | 240420→246960 | two_sided_in_range | `0x449c9d8d48dd2e5472eb7225cd5a4c57bbdc19aa1884f88d8a1e2756ee85aefc` |
| CEL | 4 | Mint | 246597 | `0x0ebfd95fb8f5b78878491c06e9f8ad1a495ea51d` | `0x0ebfd95fb8f5b78878491c06e9f8ad1a495ea51d` | 238260→244140 | two_sided_in_range | `0xd0f5a0b6415cd558f0cc0d465d6531719391b080e79fd0c60101d766ea0ec27b` |
| CEL | 5 | Mint | 226780 | `0x7328abfa5a662e583eef0ed5836a2469202467a2` | `0x7328abfa5a662e583eef0ed5836a2469202467a2` | 243000→258900 | two_sided_in_range | `0x6271ec6dadad4a2e577f553acb4ef8e8599d7344434733a8e8f662af67f005f8` |
| CEL | 5 | Burn | — | `0x7328abfa5a662e583eef0ed5836a2469202467a2` | `unavailable` | 243000→258900 | two_sided_in_range | `0x7e2cb836518f9e24528cf6bcd5beb1ac3dcda223d74c1f8a1b60edff9540910a` |

## Interpretation boundary

Owner is resolved at the transaction block when possible. No common-control claim is made across different owner addresses or tokenIds. Hour-close price classifies the range approximately; exact intra-block price may differ.
A shared Position Manager pool owner is not treated as the LP identity; tokenId, owner-at-block, and transaction sender are reported separately.
