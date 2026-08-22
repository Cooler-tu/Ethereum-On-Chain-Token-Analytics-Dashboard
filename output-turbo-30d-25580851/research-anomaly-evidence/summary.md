# Matched-pool anomaly evidence bundle

- Pool: `0x7baece5d47f1bc5e1953fbe0e9931d54dab6d810`
- Blocks: `25684865`–`25720864`
- UTC window: `2026-08-05` through `2026-08-09`
- Transfer/balance reconciliation: **exact**

## Four-ledger daily view

| Date | Swap sell / buy | Actual transfer net | LP add / remove | Residual | Matched remove→mint | +1d | +2d | +3d |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-08-05 | 5.825M / 4.487M | -4.261M | 96.225M / 101.815M | -0.009M | 10 (89.4%) | -1.85% | -2.43% | +2.59% |
| 2026-08-06 | 6.698M / 4.689M | 5.145M | 52.339M / 49.186M | -0.017M | 2 (43.4%) | -0.59% | +4.53% | +10.13% |
| 2026-08-07 | 1.039M / 2.166M | -4.845M | 0.000M / 3.719M | 0.000M | 0 (0.0%) | +5.15% | +10.78% | +6.93% |
| 2026-08-08 | 0.079M / 0.669M | 9.902M | 152.113M / 141.621M | 0.000M | 11 (81.9%) | +5.36% | +1.70% | -2.25% |
| 2026-08-09 | 2.494M / 3.374M | -10.456M | 98.437M / 108.013M | 0.000M | 6 (55.8%) | -3.47% | -7.23% | -8.02% |

Positive transfer net means TURBO entered the pool; negative means it left the pool.
Forward returns use the daily WETH-per-TURBO close, so they are ETH-relative, not USD returns.
Residual is actual Transfer net minus signed Swap net minus raw Mint/Burn principal net; it can include collected fees or other pool movements.

## Remove→mint candidates

- Matched cycles: **29**
- Gross removed: **404.354M**
- Removed amount covered by matched cycles: **288.656M (71.4%)**

| Remove tx | Mint tx | Blocks / seconds | Ticks | Removed / minted | Liquidity recreated |
|---|---|---:|---:|---:|---:|
| `0x5c3874253744f406e9170ad529098cb9953cb8ececa86a2d895cb4d0763d0aa5` | `0x0b687b20593c2fe2b261bf4064c93501f68b0905886302a3a8ef3e6e2a991adf` | 5 / 60 | -146400→-146000 | 10.807M / 10.794M | 99.88% |
| `0x7ce77bd5ec9230c5124d06d65b4a71e48f721f34d7ef8aaa101220be3becb182` | `0xf23dc449b3ed54251888b17118e777ef8ea3e535fbca3d22d49b9f240cfbf665` | 2 / 24 | -146400→-146000 | 10.807M / 10.780M | 99.76% |
| `0x5e70dbcb9dae613ea45a5e27d757250de39ec383be3cba8d073a07b7550212ef` | `0x35d9e5357fac009ef0689649f9ac541330eb6ed56ab730458d996a7f4fcf93eb` | 178 / 2148 | -146400→-146000 | 10.802M / 10.787M | 99.86% |
| `0xc8a88bf9205ff663c831b4a378e4cf9492e0f9bcaa518eb82420ebd5e393fdce` | `0x7b5e665f933d0016ee5ba6a4f71d9eff5339ddc975e0b3293c50a9d72e30abfd` | 4 / 48 | -146400→-146000 | 10.794M / 10.807M | 100.12% |
| `0x3375dbdf69922a3d1d3529098cc55497bbc0a041a44c1c800ac4fec118455064` | `0xbd74fc9ab885c864513b6c696adc13971402839ea85889c8ea77c1f56d68b77c` | 4 / 48 | -146400→-146000 | 10.767M / 10.807M | 100.36% |
| `0x979c17f33843f114a80a477d462bc973c71a6e055fc9a05e9dd1f2fba10d5083` | `0x43923d1d808106f4d10cffe3400217a524d3b8158e4834d25449b410a9796cda` | 35 / 420 | -146400→-146000 | 10.728M / 10.767M | 91.12% |
| `0xe1a1156bd601c3e242a2825bed725c165b993bab1756394b4553a0da37770261` | `0xa54da2b66a1da8b0b74bb6b27ce3004be09af63a977777dc902f59013a78d86a` | 25 / 312 | -146800→-146400 | 10.722M / 10.715M | 99.94% |
| `0x06f9ff297923f044d9926e0941c50572f976f04ab656db2550897ac755140b70` | `0xdcc578ab6452a0f4800b4f957a96356bb68f02214b213af3b8de1d84657a2bbb` | 140 / 1704 | -146800→-146400 | 10.715M / 10.715M | 100.00% |
| `0x1a9a74d91b8a561d866e3aed65fac7615fc53d97979563f4f26b899e00480822` | `0x0979661c0f682c230e5f9058d40a78cd20bcea894d4d8c263194b65498713588` | 30 / 372 | -146800→-146400 | 10.715M / 10.703M | 99.88% |
| `0xd278e08fdc327e8564002ecfa1c699cd1789959f6c0a21fb01981aa7e0238597` | `0x87415a6bdb303f8153a930e64b937a99cbe940ea5bafd2e9b844f2b35a7edf47` | 33 / 396 | -146800→-146400 | 10.703M / 10.690M | 99.88% |
| `0xc6418c6b3c9b6782425989945c8ce04dd1ea5b8adab587f3c2969171737a596b` | `0x51f475d72af884ea1a7bf1c7f1ef2d0f3b237536e4d0b127a77aef093b5e2b81` | 108 / 1296 | -146800→-146400 | 10.690M / 10.677M | 99.88% |
| `0xbeaf0845a40ab7d40901f783ba7765eea56e13c171590d6345c1a15114c3b3b4` | `0xe39770c73f59ee4e1f3b564753f0f443bb3a48c9d75abe6e377735a0c36aaf6c` | 82 / 996 | -146800→-146400 | 10.690M / 10.677M | 105.95% |
| `0xf4231d849276217cde119626f9e64963920d8ba6ca093ea16efcb77f5c01615c` | `0x44e7cc46688663413af1e4b67dbdb1aa1d26582674e7cc38ecb257a2c54f6986` | 149 / 1788 | -146800→-146400 | 10.677M / 10.670M | 99.94% |
| `0x1f93755d817e31358d6df811a5ce37613e9f0b35c3b57cc019c305ae966bc279` | `0x3d825e72375337445ba635c1db9a439380e99ddfa6fcfe9f6ba88b28144bbedb` | 30 / 360 | -146600→-146200 | 10.677M / 10.664M | 99.88% |
| `0xfb33d364475fe427676f6a32e0d6e10d0b00cc665729988183b209eba2221f53` | `0x94398571a8974abf5d18c4dff61e310b3d925531430b594df16673285d1fe01a` | 16 / 192 | -146800→-146400 | 10.670M / 10.670M | 100.00% |
| `0x0ccdc00aa334f4588000fd834a96815a56bb9fedb3cdc616e7e66cb04d957c27` | `0x7a1b3d8bcdfb374e1cb244b3e408f0fcd9f30ece118e375d39e7b952db570c37` | 70 / 852 | -146800→-146400 | 10.670M / 10.690M | 100.18% |
| `0xaf5f2ec054066c2952171d17050cc6306a6163c1658b816b5405b570cab0ae5b` | `0x32bea50d4014a99a0996eaed236d5e37db4a21595fcd479911e38ab1d7f86cdb` | 38 / 456 | -146600→-146200 | 10.664M / 10.588M | 99.29% |
| `0x19cda980fd9a0873455ea22c0ff1f5faed0749429f1cda7eab5e1088fae82d44` | `0x1ca84b13fbf827bcd1bc616a96458ac49c9caa072998e7d1405fc2b557e8d16c` | 175 / 2100 | -146600→-146200 | 10.535M / 10.664M | 93.04% |
| `0xe2aae81fc3387432cc76640e0f5eb343ebe22da3b6ec93414a7a97137caf7026` | `0xc93ec1397f2bff4580221d0999dba726868dddf091c4b042320940e57c831e89` | 53 / 648 | -146600→-146200 | 10.500M / 10.488M | 111.30% |
| `0xc39529b20bbfd6ba4d3c6d5000feae61dff08d0bfcd4ff4056ebe100e1c9ad65` | `0x2a5779789c0d5e2787e97c6109a9dfe9f1ba5d441c4d62830a86ea54780bd5ae` | 1 / 12 | -146400→-146000 | 10.317M / 10.306M | 99.88% |

## Evidence reading

- **71.4%** of gross removed target-token amount was followed by a matched pool-position-key Mint under the strict one-hour / similar-liquidity rule.
- This makes gross removal primarily an activity/cycling measure in this window; use net LP flow and actual Transfer net to identify real inventory exit.
- The exact Transfer/balance reconciliation makes actual Transfer net the cash-flow control ledger. Swap direction alone misses non-Swap liquidity movements.
- The five-day window is transaction evidence for the pilot, not an independent statistical sample and not proof of causality.

## Interpretation boundary

A cycle match uses the same raw V3 pool position key (`owner`, `tickLower`, `tickUpper`), a later Mint within the configured block gap, and similar liquidity. When `owner` is the shared NonfungiblePositionManager, this does **not** prove that the same wallet or NFT position performed both actions. Beneficial-owner attribution requires a targeted Position Manager/NFT trace.

Gross removal is activity, not permanent exit. Actual ERC-20 Transfer net flow and the end-minus-start pool balance are the cash-flow control ledger.
