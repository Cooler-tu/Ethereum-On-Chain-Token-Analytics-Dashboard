# On-Chain Token Crash & Liquidity Risk Report

## Executive Summary

- **Token:** uPEG ([0x44b28991...125505](https://etherscan.io/address/0x44b28991B167582F18BA0259e0173176ca125505))
- **Chain:** Ethereum (Chain ID: 1)
- **Analysis Window:** Block 24996372 to 25878650
- **Incident Block:** Not specified
- **Report Generated:** 2026-09-10 13:29:58 UTC

### Risk Score

| Metric | Value |
|--------|-------|
| **Final Risk Score** | **0.1367 / 1.00** |
| **Risk Level** | **LOW** |
| Evidence Confidence | 82.00% |
| Visual | `██░░░░░░░░░░░░░░░░░░` |
| Migration Adjustment | Liquidity migration detected — reducing risk by 0.30. |


## Token Profile

| Property | Value |
|----------|-------|
| Address | [0x44b28991...125505](https://etherscan.io/address/0x44b28991B167582F18BA0259e0173176ca125505) |
| Symbol | uPEG |
| Name | Unipeg |
| Decimals | 18 (onchain) |
| Total Supply | 10000.0000 |
| Is Contract | True |
| Proxy Address | None |
| Implementation | None |
| Behavior Flags | None |


## Pool Summary

**107** verified pool(s), **0** unverified candidate(s).

| Pool Address | Protocol | Version | Token0 | Token1 | Fee | Confidence |
|-------------|----------|---------|--------|--------|-----|------------|
| [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488e5be8ec8ca1db92cbec2a1ab0775) | uniswap | v3 | 0x44b28991... | 0xC02aaA39... | N/A | 100.00% |
| [0x21ff5cf7...bc0078](https://etherscan.io/address/0x21ff5cf76f562c6fb3871b59133a9e214ebc0078) | uniswap | v2 | 0x44b28991... | 0xC02aaA39... | N/A | 100.00% |
| [0x84a69fcd...314230](https://etherscan.io/address/0x84a69fcd071d5c36ef9ca3a31b1ff3aefb314230) | uniswap | v3 | 0x44b28991... | 0xA0b86991... | N/A | 100.00% |
| [0x1f7f95f5...b2a117](https://etherscan.io/address/0x1f7f95f5d7b53df049d3215ba657b00591b2a117) | uniswap | v2 | 0x44b28991... | 0xa7D12701... | N/A | 100.00% |
| [0x7059a9f1...77a890](https://etherscan.io/address/0x7059a9f16dd2405aef3dd4f70a89127ce577a890) | uniswap | v3 | 0x44b28991... | 0xA0b86991... | N/A | 100.00% |
| [0x38f0ddc5...3fe661](https://etherscan.io/address/0x38f0ddc5e8c7dc5cc820bdb0204850e7743fe661) | uniswap | v3 | 0x11111126... | 0x44b28991... | N/A | 100.00% |
| [0x0a31e71c...4eaa84](https://etherscan.io/address/0x0a31e71c45b5f624d44c97689df42564b34eaa84) | uniswap | v3 | 0x44b28991... | 0xD03FB35e... | N/A | 100.00% |
| [0x1441ffb9...131362](https://etherscan.io/address/0x1441ffb9ee7700cc7ed3692856f5267174131362) | uniswap | v3 | 0x44b28991... | 0xD03FB35e... | N/A | 100.00% |
| [0x11242c90...afa6f8](https://etherscan.io/address/0x11242c90da9ab6e673c57cf41b81418c30afa6f8) | curve | v2 | 0x44b28991... | 0xC02aaA39... | N/A | 100.00% |
| [0x52180798...f7f698](https://etherscan.io/address/0x52180798aa05745aceff7e487e54845ae4f7f698) | uniswap | v3 | 0x44b28991... | 0xD03FB35e... | N/A | 100.00% |
| [0xdefcfed7...50c0f0](https://etherscan.io/address/0xdefcfed72b78099ca4a213614348c0057c50c0f0) | uniswap | v2 | 0x44b28991... | 0xA3E78337... | N/A | 100.00% |
| [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | uniswap | v4 | 0x00000000... | 0x44b28991... | 10000 | 100.00% |
| [0xc28dd8d8...b54433](https://etherscan.io/address/0xc28dd8d8f8d1eaca22fb881602122aed85002e1cc2e8b14c9cfa18bffeb54433) | uniswap | v4 | 0x00000000... | 0x44b28991... | 9500 | 100.00% |
| [0x2a1c3953...59cd21](https://etherscan.io/address/0x2a1c3953050d960207992c60878c7371cfab656c2e55c61d10c2a8693559cd21) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 20000 | 100.00% |
| [0xb7c869a2...1acfce](https://etherscan.io/address/0xb7c869a2daedbdb2dcc5957d42c7e1385da91298483036bd517b82f81d1acfce) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9880 | 100.00% |
| [0x37000483...a6fac1](https://etherscan.io/address/0x370004836a5867fef3de3a94b5abd10081c5558c86a7e53f0cde312139a6fac1) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 11220 | 100.00% |
| [0x988d0e04...2d5002](https://etherscan.io/address/0x988d0e049acb602555383fb8742432daa8d9928e8dc8e9d2b7d25766932d5002) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9660 | 100.00% |
| [0x98690b7a...ac737c](https://etherscan.io/address/0x98690b7a207b0b1b1bc275be7f4442a69c4624478b19c38dc2ecdd270cac737c) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 30000 | 100.00% |
| [0xa28b1e42...83373f](https://etherscan.io/address/0xa28b1e4224e9096d88da48b9a884b77dde28b3434490738964d81f4b8683373f) | uniswap | v4 | 0x00000000... | 0x44b28991... | 100000 | 100.00% |
| [0x18aeda83...35ec7a](https://etherscan.io/address/0x18aeda83c51876cab01f5896839c9863d7fb30ca024e4479cc4984e7d835ec7a) | uniswap | v4 | 0x00000000... | 0x44b28991... | 60000 | 100.00% |
| [0xb9fb10f0...8f0c04](https://etherscan.io/address/0xb9fb10f0e0bd7f4def1802826e9c8ab0b19ac1b8312569a8b5fc6574088f0c04) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 18500 | 100.00% |
| [0xb012158e...fa401b](https://etherscan.io/address/0xb012158ed2a12fa4d54d6078fd19dc2ff2b8b479f039fb430639e7b8b3fa401b) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 33600 | 100.00% |
| [0x3013c855...c392bc](https://etherscan.io/address/0x3013c855e97b2861b67fc8ec4508dd8b53fda4279a2a7befe3aba68595c392bc) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 9156 | 100.00% |
| [0x2b19b55e...983a9e](https://etherscan.io/address/0x2b19b55ee60ebf4bddda01f9b59f4e11987e74db3d2831837289918efe983a9e) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 300000 | 100.00% |
| [0x42567436...9a6a4c](https://etherscan.io/address/0x42567436737c72a63d500e0eb7e966c18fdfbf8e79eca8e71159db655f9a6a4c) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 19110 | 100.00% |
| [0x9c97f57d...15e155](https://etherscan.io/address/0x9c97f57d2ec2f439955e227fbefc3c959156153c076aadb7bc4d7522a415e155) | uniswap | v4 | 0x00000000... | 0x44b28991... | 700000 | 100.00% |
| [0x3bf9b563...607f74](https://etherscan.io/address/0x3bf9b5634cc2d0656a96e1eee87c66b9d112e6b84fd6c01c7c30ce9518607f74) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 13333 | 100.00% |
| [0x8c491203...060d1a](https://etherscan.io/address/0x8c491203056268a09b4e7dd44412264d549098ff91bf517987f8d77835060d1a) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 6600 | 100.00% |
| [0xd3bf4d22...4c2956](https://etherscan.io/address/0xd3bf4d2291bdc3898f5e41dcbd0e75e136ff7876c6e082bbbde78af40b4c2956) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 8900 | 100.00% |
| [0xe15f9f3f...82ccab](https://etherscan.io/address/0xe15f9f3f3240058b21ad4419f9d3e0804ee4b71ca51b77e8ea119836ba82ccab) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9999 | 100.00% |
| [0x26e8261c...5a4585](https://etherscan.io/address/0x26e8261cc6818e69e7926023caac645ffbce078c293ffa53503a3f7a965a4585) | uniswap | v4 | 0x00000000... | 0x44b28991... | 19900 | 100.00% |
| [0x66a7c996...e472bf](https://etherscan.io/address/0x66a7c996260db9c004543c1c89590cda18a5da4d46d7c55b539a3e3451e472bf) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 770000 | 100.00% |
| [0x294e13af...6aff50](https://etherscan.io/address/0x294e13af91517ae55dce220995256ce91354c706e149c42ece7b2e832c6aff50) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9400 | 100.00% |
| [0x5c6fd7f6...c83c1b](https://etherscan.io/address/0x5c6fd7f61ee184fdad2806fd545999deb652d93f8860b5b9612bd0363dc83c1b) | uniswap | v4 | 0x00000000... | 0x44b28991... | 19000 | 100.00% |
| [0x671b836d...8b9cbc](https://etherscan.io/address/0x671b836ddc053ac124488ddbb6df9dca252d2f371dbeabbeb8014330b28b9cbc) | uniswap | v4 | 0x44b28991... | 0x6B175474... | 590000 | 100.00% |
| [0x259d3ac6...9850ee](https://etherscan.io/address/0x259d3ac6dc6d22ac5aebdba55ba32bf3bcc5dd62b954d4873b2cd562259850ee) | uniswap | v4 | 0x00000000... | 0x44b28991... | 9000 | 100.00% |
| [0xf270c08e...a92765](https://etherscan.io/address/0xf270c08ef034d21c6876fafe98d3eb52bacbecf079b5ad7e7726fac440a92765) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 990010 | 100.00% |
| [0xa871c003...c920ea](https://etherscan.io/address/0xa871c0036ce8c1924b270d0959b53c9dbee487daf838e8b18d461a920dc920ea) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9300 | 100.00% |
| [0x84c001af...2cae6b](https://etherscan.io/address/0x84c001afaadf5a6274c193f407fb46bf506bd2bba26adf445449db0fa82cae6b) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9770 | 100.00% |
| [0x164b050a...378b98](https://etherscan.io/address/0x164b050a0bf1cf6ab681b816079c8189c3f5c85cda7c56018b190c4773378b98) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9180 | 100.00% |
| [0xe7e394a4...c35a85](https://etherscan.io/address/0xe7e394a49ecc14872b8c9d46c08a3f3f11f260a7551cca4f603756990bc35a85) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9200 | 100.00% |
| [0x107f141b...ba5068](https://etherscan.io/address/0x107f141b19cfd7af731a703879804f76faf149306401e20b79e7658628ba5068) | uniswap | v4 | 0x00000000... | 0x44b28991... | 8000 | 100.00% |
| [0x5b79ce32...935ce8](https://etherscan.io/address/0x5b79ce32645ec46aaa51307802960b489f0fd56b08040150c8c993d554935ce8) | uniswap | v4 | 0x00000000... | 0x44b28991... | 19999 | 100.00% |
| [0x94bf9aab...a2229c](https://etherscan.io/address/0x94bf9aab89d34e08f4d44a2943891fa62588e8d8f1f41a573a2feea93ca2229c) | uniswap | v4 | 0x00000000... | 0x44b28991... | 20001 | 100.00% |
| [0x068b37a4...4e683a](https://etherscan.io/address/0x068b37a47765f2e31627c393a6c2d98b02074513d3d21b6cae83c3ebed4e683a) | uniswap | v4 | 0x00000000... | 0x44b28991... | 19998 | 100.00% |
| [0x92769929...b9adba](https://etherscan.io/address/0x92769929ecff6d161308b015e7670b328804fcfed576456c2cae9767fbb9adba) | uniswap | v4 | 0x00000000... | 0x44b28991... | 3000 | 100.00% |
| [0x441bab9a...587efc](https://etherscan.io/address/0x441bab9a4fcd0b66c468f5c95da009df2afb4c643fe5896d6f1bdbe0e7587efc) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 49600 | 100.00% |
| [0x544d6610...a8b319](https://etherscan.io/address/0x544d66103b8d3e6c255af7c28ba9966d316185082d2c875cefc7422672a8b319) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 48860 | 100.00% |
| [0xc8937427...817ea4](https://etherscan.io/address/0xc8937427429afbceb80f241231f8379a7887477b658c4bbcae75feedc9817ea4) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 48880 | 100.00% |
| [0x764cae8c...287851](https://etherscan.io/address/0x764cae8c179a641f7243730f38ab8a9d67bd03bac7bb621d88c94681e0287851) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9110 | 100.00% |
| [0x119cc2ad...8fe8e1](https://etherscan.io/address/0x119cc2add902dda084da03214a3235885483912cd0ec4fe3be976d94c48fe8e1) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9123 | 100.00% |
| [0xc6cea777...0af3b4](https://etherscan.io/address/0xc6cea77726a4cfb835390801451b9abe851e4050a9fa8a0e2eea339f880af3b4) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 23990 | 100.00% |
| [0x8877375e...b905eb](https://etherscan.io/address/0x8877375e74d6fbdc8a9eb13965e700978706f84c03eb3d77a268404fb5b905eb) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 66600 | 100.00% |
| [0x59d5a838...1498d3](https://etherscan.io/address/0x59d5a83844df52e9495e6c885b9c07130e13f28d02347a33755eb5c72b1498d3) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 19998 | 100.00% |
| [0xa944c7cf...bb7a1d](https://etherscan.io/address/0xa944c7cf77b6888f13b6fa3748e12dc7d57334237144d6df017bbaf7c9bb7a1d) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9960 | 100.00% |
| [0x7a56c469...e96e4b](https://etherscan.io/address/0x7a56c469e9727bbb01e0f42055803949e23609b2d632b0431c92f558a4e96e4b) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9920 | 100.00% |
| [0xd470e768...627060](https://etherscan.io/address/0xd470e7683562410bf7c285d397b406cf95c4bb1fe76d9f62c28c6dc219627060) | uniswap | v4 | 0x00000000... | 0x44b28991... | 7800 | 100.00% |
| [0x5615ef19...d28194](https://etherscan.io/address/0x5615ef19f5d58bf6978c08015b7b5aa77f0621a00836e346c9cf06c9a6d28194) | uniswap | v4 | 0x44b28991... | 0xc50673ED... | 50000 | 100.00% |
| [0xe1dfa27c...241483](https://etherscan.io/address/0xe1dfa27c22e8a4911ce89c59c71fe0cbf837546f23dc2c49d3113fb1a8241483) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 48890 | 100.00% |
| [0x56eae85a...dd1f50](https://etherscan.io/address/0x56eae85a7de857bdc12f98393a3b0491aaaf401189a179cc709ceba3b5dd1f50) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9188 | 100.00% |
| [0xae5bae18...404fbd](https://etherscan.io/address/0xae5bae18a16bd7a28c1b03f24a0ac2f388fcad823e15eaffe31f8b463f404fbd) | uniswap | v4 | 0x00000000... | 0x44b28991... | 6600 | 100.00% |
| [0xab5f53b6...69a365](https://etherscan.io/address/0xab5f53b6bc7e9ca014489e1c1595517fa4d94b4872ffb023206de0899069a365) | uniswap | v4 | 0x44b28991... | 0xC02aaA39... | 10000 | 100.00% |
| [0x47ef2bd0...f6809c](https://etherscan.io/address/0x47ef2bd048f889c7091404560b06be10e1031c5541ecc20cd255a85c0ff6809c) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9300 | 100.00% |
| [0x544996a0...2e9685](https://etherscan.io/address/0x544996a0f41bce0871fa4485d4f8835a65d7d0d7a99f5d72eb0957e6772e9685) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9100 | 100.00% |
| [0x706d677b...66bd32](https://etherscan.io/address/0x706d677bba3b0a0ddff09678269e43c060c9b7263fd702f50e1f6f6b0466bd32) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9310 | 100.00% |
| [0x597235f2...99a47e](https://etherscan.io/address/0x597235f24354d6508e778666fe95feb432eeb341766df2937f2dfc124299a47e) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 9919 | 100.00% |
| [0x9eb7d053...bee490](https://etherscan.io/address/0x9eb7d0531440d7520f3b5dde36bf0053be8497c99f323ea953dd86bcdebee490) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9000 | 100.00% |
| [0xaacaafb4...3e0100](https://etherscan.io/address/0xaacaafb47e412e1a8a15a698906690acac58cbc187199b3cda7d8cbe7a3e0100) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9100 | 100.00% |
| [0x6fe1e0ed...d8d1fa](https://etherscan.io/address/0x6fe1e0edb697f1e215c3cdcbbd8f9a4564e489458300d2b3c4b3720a9dd8d1fa) | uniswap | v4 | 0x44b28991... | 0x829f4B62... | 10000 | 100.00% |
| [0x64e37a74...70a950](https://etherscan.io/address/0x64e37a74f16260bf7e129738c97555bee0ffc8031309f701deafbbc26d70a950) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9800 | 100.00% |
| [0x5f7e34c1...2e790a](https://etherscan.io/address/0x5f7e34c11e013d3e4705ba97a0aada2af1310f4bb355451f08e3317a332e790a) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 24700 | 100.00% |
| [0xc3a40cd2...a95e69](https://etherscan.io/address/0xc3a40cd218b9be0669384c7f9f3390ba1489b2d72ac9102135eeb12991a95e69) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 9198 | 100.00% |
| [0x00c70fc4...6263de](https://etherscan.io/address/0x00c70fc4efec0f8cef6330825bdff9dd1fd07face3826ee7bfe3ba46266263de) | uniswap | v4 | 0x44b28991... | 0x553e2f66... | 10000 | 100.00% |
| [0x3e14a5d5...ad002e](https://etherscan.io/address/0x3e14a5d55b76b4ad9b698809721e11dce6c48e53c8e65a40f68b493cfdad002e) | uniswap | v4 | 0x00000000... | 0x44b28991... | 5000 | 100.00% |
| [0x1235a283...ed389e](https://etherscan.io/address/0x1235a283238d61b99e68a912095405df4d7e4ec8756e6877c0fe6e035aed389e) | uniswap | v4 | 0x00000000... | 0x44b28991... | 10000 | 100.00% |
| [0x27aa4d6c...3733b3](https://etherscan.io/address/0x27aa4d6cc3ffe76b1cffc1a421788bba00091d96daac5e6c0e7127348a3733b3) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 8996 | 100.00% |
| [0x3384eed0...6ad684](https://etherscan.io/address/0x3384eed0895713f29074d59bd375d099f0f54756d12390a76c3eb5352b6ad684) | uniswap | v4 | 0x44b28991... | 0x6E3Ab19A... | 0 | 100.00% |
| [0xf1797ebb...0ff639](https://etherscan.io/address/0xf1797ebb2fea5a6f9a834bd95a3da9119b9f93cd57261352f2763f1fba0ff639) | uniswap | v4 | 0x44b28991... | 0x4c5de819... | 10000 | 100.00% |
| [0x952155ca...a8fa23](https://etherscan.io/address/0x952155ca1ffb8832cf9546fea165ac01c70eec983f8d637ba156e55c58a8fa23) | uniswap | v4 | 0x00000000... | 0x44b28991... | 5000 | 100.00% |
| [0x6fc16e0c...d5d472](https://etherscan.io/address/0x6fc16e0c34e21b9656257d6af773bd31e4b7b176331bfb8abde0f65d04d5d472) | uniswap | v4 | 0x44b28991... | 0xc0F8F4C9... | 0 | 100.00% |
| [0x20f992d4...dbde28](https://etherscan.io/address/0x20f992d417c418925bad4d8cd8915b663c1816fc727550c72fb131b861dbde28) | uniswap | v4 | 0x44b28991... | 0xD03FB35e... | 10000 | 100.00% |
| [0x678c78df...1bb543](https://etherscan.io/address/0x678c78dfeed678e2d8da417d1b98d06707aae6eddc6cdbff3c9c46248a1bb543) | uniswap | v4 | 0x44b28991... | 0xD03FB35e... | 3000 | 100.00% |
| [0xda380ea1...bf1499](https://etherscan.io/address/0xda380ea1bfe73049446db00ebedac5e76e846211340208bc1bcf9be0c6bf1499) | uniswap | v4 | 0x44b28991... | 0xD03FB35e... | 500 | 100.00% |
| [0x90d25b98...b83f81](https://etherscan.io/address/0x90d25b9897e6f633e7eb390c1e71d02fd54febcf92641d1c391847d4b4b83f81) | uniswap | v4 | 0x44b28991... | 0xbd3AB585... | 50000 | 100.00% |
| [0x677bb32b...fc2af3](https://etherscan.io/address/0x677bb32b208acd22856cd2dcb376eff9a85880e66cac09927248bba41efc2af3) | uniswap | v4 | 0x00000000... | 0x44b28991... | 8900 | 100.00% |
| [0x37dd5fc1...e3a97a](https://etherscan.io/address/0x37dd5fc1aee07df4e78bb86c843509ebbde9fe3bc193e73351449f0a2de3a97a) | uniswap | v4 | 0x44b28991... | 0xbd3AB585... | 20000 | 100.00% |
| [0xa642d816...c30bff](https://etherscan.io/address/0xa642d816319bc87b6266aaa218b163cabe59d2d96924208f5d3e2d8692c30bff) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 770000 | 100.00% |
| [0x2d0bb294...37e9fa](https://etherscan.io/address/0x2d0bb294ea49f72ae7c1dbadfa0cea78108ab5acc4d6ad7b958f4551c237e9fa) | uniswap | v4 | 0x44b28991... | 0xf819d9Cb... | 10000 | 100.00% |
| [0x44f8b994...4aa4ef](https://etherscan.io/address/0x44f8b9941effdb5bdab4000175be02890ecc5ba907ee3a6e2eb5a1e9aa4aa4ef) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 880000 | 100.00% |
| [0x81470319...1ed2bf](https://etherscan.io/address/0x81470319d6b009e72e87a18ec09192f530983b651792403acacf4bb4d41ed2bf) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 3000 | 100.00% |
| [0xf5596d2f...70333e](https://etherscan.io/address/0xf5596d2ffc4934ae18457271fd1fb0f5fd17edc7fea2092d75849004ab70333e) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 28880 | 100.00% |
| [0xa3aa37b2...5fc3de](https://etherscan.io/address/0xa3aa37b2c783907f3d0d1be7b0ee27dd505bfbf0e5b1c33c9eb1c1528e5fc3de) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 26880 | 100.00% |
| [0x896d9f18...b27200](https://etherscan.io/address/0x896d9f18b2ab2ddd57ff8ff09579cb2a3569d74c40386d180f4cb12635b27200) | uniswap | v4 | 0x44b28991... | 0xD03FB35e... | 50000 | 100.00% |
| [0xaa9c8442...5969a1](https://etherscan.io/address/0xaa9c844241d57dfc5fbc2121967953fbaff46aa6e2c388e5e556d399595969a1) | uniswap | v4 | 0x2940446b... | 0x44b28991... | 9000 | 100.00% |
| [0x610c465e...12c0bf](https://etherscan.io/address/0x610c465ebaca5882871b663fa5a799985a97369edca42d1747ca98032412c0bf) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 18900 | 100.00% |
| [0xa6e8b4a5...c780e1](https://etherscan.io/address/0xa6e8b4a597d0ee92b85d91fcc686e46640af729fba3fdeab11dcefd117c780e1) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 22500 | 100.00% |
| [0xe204520a...079ed1](https://etherscan.io/address/0xe204520a24510e25833800f5865278bc70c642e4007cf1fdc76946f6fd079ed1) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 24200 | 100.00% |
| [0x6485175e...95ae7f](https://etherscan.io/address/0x6485175eada7bb0dd4ea0143d4cf9b94ba26f55040510b875d229fab3d95ae7f) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 28800 | 100.00% |
| [0xda43c52f...425a2c](https://etherscan.io/address/0xda43c52f98f5062aa46c3e01cb8aaa50ed5aa2e59ee59bbf1882cfce0e425a2c) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 5000 | 100.00% |
| [0xe156c933...8f2b7d](https://etherscan.io/address/0xe156c9333568eb82e138a1ad624d16a286d54f622a2501b0da48e7f6168f2b7d) | uniswap | v4 | 0x00000000... | 0x44b28991... | 1500 | 100.00% |
| [0x9d3d46f9...26a3bb](https://etherscan.io/address/0x9d3d46f9fab851872820d3cc4b2f839fa11de03f2b9b11224d7e7b250026a3bb) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 25000 | 100.00% |
| [0x209640d8...193d4b](https://etherscan.io/address/0x209640d8d1f04d27df064f2335a64db8138f79190dcea447f445683ed8193d4b) | uniswap | v4 | 0x44b28991... | 0xdAC17F95... | 15000 | 100.00% |
| [0xe05147bb...459519](https://etherscan.io/address/0xe05147bbe9d8dad6e9e0a9a61daf322c4839dc9a7422850fed19829d5f459519) | uniswap | v4 | 0x00000000... | 0x44b28991... | 250 | 100.00% |
| [0x5c8ae631...6396e8](https://etherscan.io/address/0x5c8ae63113f673a5c3d60815d53e772fe39098eb386481c4c654b921a36396e8) | uniswap | v4 | 0x00000000... | 0x44b28991... | 1500 | 100.00% |
| [0x300e285c...12de8f](https://etherscan.io/address/0x300e285c2e11cdb33ea124c2b08e3c516bcf6a998f2299665dad29e1cb12de8f) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 29750 | 100.00% |
| [0x6ae0d777...9f47a7](https://etherscan.io/address/0x6ae0d7772317f3faa3a724b9332abf1dba49f184785afe6d631d728fce9f47a7) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 29950 | 100.00% |
| [0xe367022b...e3d193](https://etherscan.io/address/0xe367022be965e53b4c03083a85f8ff0edc81852f0ffbf107287cdf2b2ce3d193) | uniswap | v4 | 0x44b28991... | 0xA0b86991... | 28860 | 100.00% |


## Related Addresses

| Address | Label | Category | Confidence |
|---------|-------|----------|------------|
| [0x1F98431c...31F984](https://etherscan.io/address/0x1F98431c8aD98523631AE4a59f267346ea31F984) | Factory (uniswap)_v3 | protocol_deployment | 100% |
| [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488E5BE8eC8CA1Db92CBEc2a1ab0775) | Uniswap V3 Pool | pool | 100% |
| [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | PositionManager (uniswap_v3) | position_manager | 100% |
| [0xE592427A...861564](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564) | Router (uniswap_v3) | router | 100% |
| [0x5C69bEe7...c5aA6f](https://etherscan.io/address/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f) | Factory (uniswap)_v2 | protocol_deployment | 100% |
| [0x21ff5cf7...Bc0078](https://etherscan.io/address/0x21ff5cf76f562c6fb3871b59133a9E214eBc0078) | Uniswap V2 Pool | pool | 100% |
| [0x7a250d56...F2488D](https://etherscan.io/address/0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D) | Router (uniswap_v2) | router | 100% |
| [0x84a69fcD...314230](https://etherscan.io/address/0x84a69fcD071D5c36EF9ca3A31b1ff3aEFB314230) | Uniswap V3 Pool | pool | 100% |
| [0x1f7f95f5...B2A117](https://etherscan.io/address/0x1f7f95f5D7b53dF049d3215ba657B00591B2A117) | Uniswap V2 Pool | pool | 100% |
| [0x7059A9f1...77a890](https://etherscan.io/address/0x7059A9f16dd2405AeF3Dd4f70a89127Ce577a890) | Uniswap V3 Pool | pool | 100% |
| [0x38f0DDC5...3Fe661](https://etherscan.io/address/0x38f0DDC5E8c7DC5cc820bDB0204850E7743Fe661) | Uniswap V3 Pool | pool | 100% |
| [0x0a31E71c...4eaa84](https://etherscan.io/address/0x0a31E71c45B5f624d44c97689dF42564b34eaa84) | Uniswap V3 Pool | pool | 100% |
| [0x1441FFB9...131362](https://etherscan.io/address/0x1441FFB9Ee7700CC7Ed3692856F5267174131362) | Uniswap V3 Pool | pool | 100% |
| [0x90E00ACe...c2d7f5](https://etherscan.io/address/0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5) | Factory (curve)_v2 | protocol_deployment | 100% |
| [0x11242C90...aFa6F8](https://etherscan.io/address/0x11242C90Da9aB6E673C57Cf41b81418C30aFa6F8) | Curve V2 Pool | pool | 100% |
| [0x52180798...f7F698](https://etherscan.io/address/0x52180798AA05745acEFF7e487E54845Ae4f7F698) | Uniswap V3 Pool | pool | 100% |
| [0xDefcFeD7...50c0F0](https://etherscan.io/address/0xDefcFeD72b78099cA4A213614348c0057c50c0F0) | Uniswap V2 Pool | pool | 100% |
| [0x00000000...E08A90](https://etherscan.io/address/0x000000000004444c5dc75cB358380D2e3dE08A90) | Factory (uniswap)_v4 | protocol_deployment | 100% |
| [0xbD216513...64ee9e](https://etherscan.io/address/0xbD216513d74C8cf14cf4747E6AaA6420FF64ee9e) | PositionManager (uniswap_v4) | position_manager | 100% |
| [0x66a9893C...Dd6748](https://etherscan.io/address/0x66a9893Cc07d91d95644cfDcE5591279A7Dd6748) | Router (uniswap_v4) | router | 100% |
| [0x00000000...E08A90](https://etherscan.io/address/0x000000000004444c5dc75cB358380D2e3dE08A90) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x163F3103...1856E0](https://etherscan.io/address/0x163F3103De041d25464E2C8A4f8f3187EC1856E0) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488E5BE8eC8CA1Db92CBEc2a1ab0775) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x6A93eF5f...97006c](https://etherscan.io/address/0x6A93eF5f666eebE84bA130F8404AD56ee197006c) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xb300000b...c7028d](https://etherscan.io/address/0xb300000b72DEAEb607a12d5f54773D1C19c7028d) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x4C82D1fB...0a2cCA](https://etherscan.io/address/0x4C82D1fBFe28C977cBB58D8C7FF8FCF9F70a2cCA) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x7f54F056...A3Be8A](https://etherscan.io/address/0x7f54F05635d15Cde17A49502fEdB9D1803A3Be8A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x67e10bF2...828B6A](https://etherscan.io/address/0x67e10bF231865CE1cc04A363c5b0ad2Bb9828B6A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x6747BcaF...dfACB5](https://etherscan.io/address/0x6747BcaF9bD5a5F0758Cbe08903490E45DdfACB5) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x66a9893c...dBA8Af](https://etherscan.io/address/0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x1231DEB6...6F4EaE](https://etherscan.io/address/0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x09AD820a...024Afa](https://etherscan.io/address/0x09AD820aaC5779683B481c4674208A4e1B024Afa) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x8F10B468...13f996](https://etherscan.io/address/0x8F10B468b06c6FD214B65F87778827F7D113f996) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xb92fe925...4fFf4f](https://etherscan.io/address/0xb92fe925DC43a0ECdE6c8b1a2709c170Ec4fFf4f) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x74de5d4F...016631](https://etherscan.io/address/0x74de5d4FCbf63E00296fd95d33236B9794016631) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x28b1Dc1a...B2a183](https://etherscan.io/address/0x28b1Dc1a5E3699A428BC51d234DFab7C9CB2a183) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xA5F91E59...B730B0](https://etherscan.io/address/0xA5F91E598668040055dC861a7316e677a5B730B0) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x7059A9f1...77a890](https://etherscan.io/address/0x7059A9f16dd2405AeF3Dd4f70a89127Ce577a890) | Frequent Token Receiver | frequent_interactor | 50% |
| [0x7D0C8447...dFCDBd](https://etherscan.io/address/0x7D0C844795f7d73ad5aAEBE1af52033621dFCDBd) | Frequent Token Receiver | frequent_interactor | 50% |
| [0xC10eE903...910fb4](https://etherscan.io/address/0xC10eE9031F2a0B84766A86B55a8D90F357910fb4) | Frequent Token Sender | frequent_interactor | 50% |
| [0x9642b23E...2F5D4E](https://etherscan.io/address/0x9642b23Ed1E01Df1092B92641051881a322F5D4E) | Frequent Token Sender | frequent_interactor | 50% |
| [0x06CFf708...d2f5ef](https://etherscan.io/address/0x06CFf7088619C7178F5e14f0B119458d08d2f5ef) | Frequent Token Sender | frequent_interactor | 50% |
| [0x00000000...00dEaD](https://etherscan.io/address/0x000000000000000000000000000000000000dEaD) | Burn Address | burn | 100% |
| [0x00000000...000000](https://etherscan.io/address/0x0000000000000000000000000000000000000000) | Burn Address | burn | 100% |
| [0x00000000...00dead](https://etherscan.io/address/0x000000000000000000000000000000000000dead) | Burn Address | burn | 100% |


## TVL & Price History

| Metric | Value |
|--------|-------|
| Total TVL (in token units) | 34.0832 |
| Active Pools | 0 |
| Main Pool | [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488e5be8ec8ca1db92cbec2a1ab0775) |
| Main Pool Share | 99.48% |


## Liquidity Events

- **Liquidity Additions:** 6574 events
- **Liquidity Removals:** 7025 events

### Significant Liquidity Removals

| Block | Timestamp | Pool | Actor | Amount0 | Amount1 |
|-------|-----------|------|-------|---------|---------|
| 24996520 | 2026-05-01 00:30:59 UTC | [0x2a1c3953...59cd21](https://etherscan.io/address/0x2a1c3953050d960207992c60878c7371cfab656c2e55c61d10c2a8693559cd21) | [0xbD216513...64ee9e](https://etherscan.io/address/0xbD216513d74C8cf14cf4747E6AaA6420FF64ee9e) | 1.4989 | 3638.21 |
| 24996626 | 2026-05-01 00:52:11 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 272.7027 | 20897599828.24 |
| 24996932 | 2026-05-01 01:53:47 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 168.6819 | 23217753912.44 |
| 24996963 | 2026-05-01 01:59:59 UTC | [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488E5BE8eC8CA1Db92CBEc2a1ab0775) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 22.2362 | 16.6101 |
| 24996979 | 2026-05-01 02:03:11 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 235.4588 | 295825891229.16 |
| 24997012 | 2026-05-01 02:09:47 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 178.0906 | 28933086433.67 |
| 24997026 | 2026-05-01 02:12:35 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 248.8823 | 0 |
| 24997088 | 2026-05-01 02:24:59 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 33.4208 | 7.2487 |
| 24997172 | 2026-05-01 02:41:47 UTC | [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488E5BE8eC8CA1Db92CBEc2a1ab0775) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 2.8846 | 272504215662.37 |
| 24997246 | 2026-05-01 02:56:47 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 207.2699 | 0 |
| 24997249 | 2026-05-01 02:57:23 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 1.3600 | 176819560257.64 |
| 24997282 | 2026-05-01 03:04:11 UTC | [0x2a1c3953...59cd21](https://etherscan.io/address/0x2a1c3953050d960207992c60878c7371cfab656c2e55c61d10c2a8693559cd21) | [0xbD216513...64ee9e](https://etherscan.io/address/0xbD216513d74C8cf14cf4747E6AaA6420FF64ee9e) | 1.2887 | 2034.84 |
| 24997284 | 2026-05-01 03:04:35 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 377.3409 | 551682203655.79 |
| 24997339 | 2026-05-01 03:15:35 UTC | [0xb9fb10f0...8f0c04](https://etherscan.io/address/0xb9fb10f0e0bd7f4def1802826e9c8ab0b19ac1b8312569a8b5fc6574088f0c04) | [0xbD216513...64ee9e](https://etherscan.io/address/0xbD216513d74C8cf14cf4747E6AaA6420FF64ee9e) | 3.3887 | 5939.41 |
| 24997374 | 2026-05-01 03:22:47 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 342.2057 | 0 |
| 24997382 | 2026-05-01 03:24:23 UTC | [0x2a1c3953...59cd21](https://etherscan.io/address/0x2a1c3953050d960207992c60878c7371cfab656c2e55c61d10c2a8693559cd21) | [0xbD216513...64ee9e](https://etherscan.io/address/0xbD216513d74C8cf14cf4747E6AaA6420FF64ee9e) | 2.0337 | 22763.31 |
| 24997395 | 2026-05-01 03:26:59 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 249.1224 | 187176017200.23 |
| 24997427 | 2026-05-01 03:33:23 UTC | [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488E5BE8eC8CA1Db92CBEc2a1ab0775) | [0xC36442b4...11FE88](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88) | 6.2436 | 11.8622 |
| 24997484 | 2026-05-01 03:44:47 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 5.7070 | 270270365297.95 |
| 24997541 | 2026-05-01 03:56:23 UTC | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0xa462d9Ac...8c27A1](https://etherscan.io/address/0xa462d9AcaCcb141Ce7F17213b95198fE248c27A1) | 275.6808 | 270239117869.67 |


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
| Pre-Crash Withdrawals | 7025 |
| Attributed Withdrawals | 3803 |
| Total Removed (uPEG) | 8120.85956544 |
| Total Removed (USD est.) | $36,470,299.44 |
| Pre-Event TVL | 34.0832 |
| Withdrawal Severity | 100.00% of pre-event TVL |

### Removals by Pool

| Pool | Events | Removed (uPEG) | Est. USD | % Pool TVL |
|------|--------|--------------|----------|------------|
| [0x7059a9f1...77a890](https://etherscan.io/address/0x7059a9f16dd2405aef3dd4f70a89127ce577a890) | 78 | 27.78067713 | $28,092,505.63 | 100.00% |
| [0xe7e394a4...c35a85](https://etherscan.io/address/0xe7e394a49ecc14872b8c9d46c08a3f3f11f260a7551cca4f603756990bc35a85) | 1001 | 1471.48020154 | $5,818,487.86 | - |
| [0x2a1c3953...59cd21](https://etherscan.io/address/0x2a1c3953050d960207992c60878c7371cfab656c2e55c61d10c2a8693559cd21) | 285 | 318.6458614 | $1,318,494.42 | - |
| [0xda43c52f...425a2c](https://etherscan.io/address/0xda43c52f98f5062aa46c3e01cb8aaa50ed5aa2e59ee59bbf1882cfce0e425a2c) | 20 | 6.78803254 | $723,838.59 | - |
| [0xa871c003...c920ea](https://etherscan.io/address/0xa871c0036ce8c1924b270d0959b53c9dbee487daf838e8b18d461a920dc920ea) | 31 | 5.12159632 | $122,700.79 | - |
| [0x119cc2ad...8fe8e1](https://etherscan.io/address/0x119cc2add902dda084da03214a3235885483912cd0ec4fe3be976d94c48fe8e1) | 1 | 0.00177315 | $50,029.43 | - |
| [0x764cae8c...287851](https://etherscan.io/address/0x764cae8c179a641f7243730f38ab8a9d67bd03bac7bb621d88c94681e0287851) | 1 | 0.01755524 | $49,996.25 | - |
| [0x8c491203...060d1a](https://etherscan.io/address/0x8c491203056268a09b4e7dd44412264d549098ff91bf517987f8d77835060d1a) | 2 | 5.27147817 | $48,584.48 | - |
| [0x988d0e04...2d5002](https://etherscan.io/address/0x988d0e049acb602555383fb8742432daa8d9928e8dc8e9d2b7d25766932d5002) | 10 | 2.36894259 | $30,800.00 | - |
| [0xb7c869a2...1acfce](https://etherscan.io/address/0xb7c869a2daedbdb2dcc5957d42c7e1385da91298483036bd517b82f81d1acfce) | 3 | 1.58901894 | $26,532.70 | - |
| [0x164b050a...378b98](https://etherscan.io/address/0x164b050a0bf1cf6ab681b816079c8189c3f5c85cda7c56018b190c4773378b98) | 2 | 0.37432624 | $21,163.32 | - |
| [0x3bf9b563...607f74](https://etherscan.io/address/0x3bf9b5634cc2d0656a96e1eee87c66b9d112e6b84fd6c01c7c30ce9518607f74) | 1 | 0.01938642 | $20,032.43 | - |
| [0x81470319...1ed2bf](https://etherscan.io/address/0x81470319d6b009e72e87a18ec09192f530983b651792403acacf4bb4d41ed2bf) | 53 | 60.57394373 | $19,610.78 | - |
| [0x98690b7a...ac737c](https://etherscan.io/address/0x98690b7a207b0b1b1bc275be7f4442a69c4624478b19c38dc2ecdd270cac737c) | 5 | 0.30521492 | $17,365.63 | - |
| [0x37000483...a6fac1](https://etherscan.io/address/0x370004836a5867fef3de3a94b5abd10081c5558c86a7e53f0cde312139a6fac1) | 1 | 2.46957089 | $16,635.97 | - |
| [0x84c001af...2cae6b](https://etherscan.io/address/0x84c001afaadf5a6274c193f407fb46bf506bd2bba26adf445449db0fa82cae6b) | 1 | 0.7248954 | $16,499.84 | - |
| [0x294e13af...6aff50](https://etherscan.io/address/0x294e13af91517ae55dce220995256ce91354c706e149c42ece7b2e832c6aff50) | 3 | 0.18350479 | $11,776.47 | - |
| [0xb9fb10f0...8f0c04](https://etherscan.io/address/0xb9fb10f0e0bd7f4def1802826e9c8ab0b19ac1b8312569a8b5fc6574088f0c04) | 2 | 3.39827161 | $10,950.70 | - |
| [0x42567436...9a6a4c](https://etherscan.io/address/0x42567436737c72a63d500e0eb7e966c18fdfbf8e79eca8e71159db655f9a6a4c) | 1 | 0.17855258 | $9,723.66 | - |
| [0xe15f9f3f...82ccab](https://etherscan.io/address/0xe15f9f3f3240058b21ad4419f9d3e0804ee4b71ca51b77e8ea119836ba82ccab) | 1 | 0.31165624 | $9,476.07 | - |
| [0x3013c855...c392bc](https://etherscan.io/address/0x3013c855e97b2861b67fc8ec4508dd8b53fda4279a2a7befe3aba68595c392bc) | 2 | 0.3684854 | $4,813.30 | - |
| [0xf5596d2f...70333e](https://etherscan.io/address/0xf5596d2ffc4934ae18457271fd1fb0f5fd17edc7fea2092d75849004ab70333e) | 1 | 0.00122638 | $2,999.79 | - |
| [0xa3aa37b2...5fc3de](https://etherscan.io/address/0xa3aa37b2c783907f3d0d1be7b0ee27dd505bfbf0e5b1c33c9eb1c1528e5fc3de) | 1 | 0.47879707 | $2,910.27 | - |
| [0x6ae0d777...9f47a7](https://etherscan.io/address/0x6ae0d7772317f3faa3a724b9332abf1dba49f184785afe6d631d728fce9f47a7) | 1 | 0.33246116 | $2,749.40 | - |
| [0x9d3d46f9...26a3bb](https://etherscan.io/address/0x9d3d46f9fab851872820d3cc4b2f839fa11de03f2b9b11224d7e7b250026a3bb) | 2 | 5.36810367 | $2,714.09 | - |
| [0xe367022b...e3d193](https://etherscan.io/address/0xe367022be965e53b4c03083a85f8ff0edc81852f0ffbf107287cdf2b2ce3d193) | 1 | 0.44914895 | $2,684.62 | - |
| [0xe204520a...079ed1](https://etherscan.io/address/0xe204520a24510e25833800f5865278bc70c642e4007cf1fdc76946f6fd079ed1) | 1 | 0.85639651 | $2,078.71 | - |
| [0x6485175e...95ae7f](https://etherscan.io/address/0x6485175eada7bb0dd4ea0143d4cf9b94ba26f55040510b875d229fab3d95ae7f) | 1 | 0.00012749 | $2,024.61 | - |
| [0x544d6610...a8b319](https://etherscan.io/address/0x544d66103b8d3e6c255af7c28ba9966d316185082d2c875cefc7422672a8b319) | 1 | 0.00564186 | $2,009.97 | - |
| [0x441bab9a...587efc](https://etherscan.io/address/0x441bab9a4fcd0b66c468f5c95da009df2afb4c643fe5896d6f1bdbe0e7587efc) | 1 | 0.00104032 | $2,001.68 | - |
| [0xa6e8b4a5...c780e1](https://etherscan.io/address/0xa6e8b4a597d0ee92b85d91fcc686e46640af729fba3fdeab11dcefd117c780e1) | 1 | 1.43530991 | $1,986.03 | - |
| [0xc8937427...817ea4](https://etherscan.io/address/0xc8937427429afbceb80f241231f8379a7887477b658c4bbcae75feedc9817ea4) | 1 | 0.29559104 | $1,725.91 | - |
| [0xb012158e...fa401b](https://etherscan.io/address/0xb012158ed2a12fa4d54d6078fd19dc2ff2b8b479f039fb430639e7b8b3fa401b) | 1 | 0.3136319 | $1,568.43 | - |
| [0x209640d8...193d4b](https://etherscan.io/address/0x209640d8d1f04d27df064f2335a64db8138f79190dcea447f445683ed8193d4b) | 1 | 2.52333773 | $1,448.70 | - |
| [0x84a69fcd...314230](https://etherscan.io/address/0x84a69fcd071d5c36ef9ca3a31b1ff3aefb314230) | 1 | 0.6376505 | $596.09 | - |
| [0xf270c08e...a92765](https://etherscan.io/address/0xf270c08ef034d21c6876fafe98d3eb52bacbecf079b5ad7e7726fac440a92765) | 1 | 0.50477046 | $335.48 | - |
| [0xd3bf4d22...4c2956](https://etherscan.io/address/0xd3bf4d2291bdc3898f5e41dcbd0e75e136ff7876c6e082bbbde78af40b4c2956) | 4 | 0.002507 | $276.36 | - |
| [0x671b836d...8b9cbc](https://etherscan.io/address/0x671b836ddc053ac124488ddbb6df9dca252d2f371dbeabbeb8014330b28b9cbc) | 1 | 0.06601514 | $171.00 | - |
| [0x259d3ac6...9850ee](https://etherscan.io/address/0x259d3ac6dc6d22ac5aebdba55ba32bf3bcc5dd62b954d4873b2cd562259850ee) | 264 | 2305.9744538 | - | - |
| [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | 618 | 1822.41915834 | - | - |
| [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488e5be8ec8ca1db92cbec2a1ab0775) | 734 | 934.88103187 | - | 100.00% |
| [0xc28dd8d8...b54433](https://etherscan.io/address/0xc28dd8d8f8d1eaca22fb881602122aed85002e1cc2e8b14c9cfa18bffeb54433) | 480 | 651.40163615 | - | - |
| [0xa28b1e42...83373f](https://etherscan.io/address/0xa28b1e4224e9096d88da48b9a884b77dde28b3434490738964d81f4b8683373f) | 105 | 228.87679833 | - | - |
| [0x107f141b...ba5068](https://etherscan.io/address/0x107f141b19cfd7af731a703879804f76faf149306401e20b79e7658628ba5068) | 21 | 85.92836504 | - | - |
| [0x677bb32b...fc2af3](https://etherscan.io/address/0x677bb32b208acd22856cd2dcb376eff9a85880e66cac09927248bba41efc2af3) | 1 | 68.74288915 | - | - |
| [0x0a31e71c...4eaa84](https://etherscan.io/address/0x0a31e71c45b5f624d44c97689df42564b34eaa84) | 4 | 39.75937471 | - | - |
| [0x21ff5cf7...bc0078](https://etherscan.io/address/0x21ff5cf76f562c6fb3871b59133a9e214ebc0078) | 8 | 11.94350065 | - | 100.00% |
| [0x20f992d4...dbde28](https://etherscan.io/address/0x20f992d417c418925bad4d8cd8915b663c1816fc727550c72fb131b861dbde28) | 7 | 9.67269401 | - | - |
| [0x5b79ce32...935ce8](https://etherscan.io/address/0x5b79ce32645ec46aaa51307802960b489f0fd56b08040150c8c993d554935ce8) | 1 | 8.8428433 | - | - |
| [0x18aeda83...35ec7a](https://etherscan.io/address/0x18aeda83c51876cab01f5896839c9863d7fb30ca024e4479cc4984e7d835ec7a) | 11 | 6.86871617 | - | - |
| [0x896d9f18...b27200](https://etherscan.io/address/0x896d9f18b2ab2ddd57ff8ff09579cb2a3569d74c40386d180f4cb12635b27200) | 2 | 6.25598741 | - | - |
| [0x94bf9aab...a2229c](https://etherscan.io/address/0x94bf9aab89d34e08f4d44a2943891fa62588e8d8f1f41a573a2feea93ca2229c) | 1 | 5.78070571 | - | - |
| [0x952155ca...a8fa23](https://etherscan.io/address/0x952155ca1ffb8832cf9546fea165ac01c70eec983f8d637ba156e55c58a8fa23) | 1 | 3.09613903 | - | - |
| [0xe156c933...8f2b7d](https://etherscan.io/address/0xe156c9333568eb82e138a1ad624d16a286d54f622a2501b0da48e7f6168f2b7d) | 1 | 2.89286122 | - | - |
| [0x90d25b98...b83f81](https://etherscan.io/address/0x90d25b9897e6f633e7eb390c1e71d02fd54febcf92641d1c391847d4b4b83f81) | 4 | 1.04830934 | - | - |
| [0x92769929...b9adba](https://etherscan.io/address/0x92769929ecff6d161308b015e7670b328804fcfed576456c2cae9767fbb9adba) | 1 | 0.99346814 | - | - |
| [0xda380ea1...bf1499](https://etherscan.io/address/0xda380ea1bfe73049446db00ebedac5e76e846211340208bc1bcf9be0c6bf1499) | 1 | 0.65815934 | - | - |
| [0x52180798...f7f698](https://etherscan.io/address/0x52180798aa05745aceff7e487e54845ae4f7f698) | 1 | 0.65181253 | - | - |
| [0x1441ffb9...131362](https://etherscan.io/address/0x1441ffb9ee7700cc7ed3692856f5267174131362) | 1 | 0.56790602 | - | - |
| [0xe05147bb...459519](https://etherscan.io/address/0xe05147bbe9d8dad6e9e0a9a61daf322c4839dc9a7422850fed19829d5f459519) | 1 | 0.55300961 | - | - |
| [0x9c97f57d...15e155](https://etherscan.io/address/0x9c97f57d2ec2f439955e227fbefc3c959156153c076aadb7bc4d7522a415e155) | 1 | 0.49382806 | - | - |
| [0x678c78df...1bb543](https://etherscan.io/address/0x678c78dfeed678e2d8da417d1b98d06707aae6eddc6cdbff3c9c46248a1bb543) | 1 | 0.36284538 | - | - |
| [0x37dd5fc1...e3a97a](https://etherscan.io/address/0x37dd5fc1aee07df4e78bb86c843509ebbde9fe3bc193e73351449f0a2de3a97a) | 1 | 0.25954014 | - | - |
| [0x1f7f95f5...b2a117](https://etherscan.io/address/0x1f7f95f5d7b53df049d3215ba657b00591b2a117) | 1 | 0.20600893 | - | - |
| [0xf1797ebb...0ff639](https://etherscan.io/address/0xf1797ebb2fea5a6f9a834bd95a3da9119b9f93cd57261352f2763f1fba0ff639) | 2 | 0.18203969 | - | - |
| [0x5c6fd7f6...c83c1b](https://etherscan.io/address/0x5c6fd7f61ee184fdad2806fd545999deb652d93f8860b5b9612bd0363dc83c1b) | 1 | 0.17189589 | - | - |
| [0xaa9c8442...5969a1](https://etherscan.io/address/0xaa9c844241d57dfc5fbc2121967953fbaff46aa6e2c388e5e556d399595969a1) | 1 | 0.07438475 | - | - |
| [0x068b37a4...4e683a](https://etherscan.io/address/0x068b37a47765f2e31627c393a6c2d98b02074513d3d21b6cae83c3ebed4e683a) | 1 | 0.03063048 | - | - |
| [0x26e8261c...5a4585](https://etherscan.io/address/0x26e8261cc6818e69e7926023caac645ffbce078c293ffa53503a3f7a965a4585) | 1 | 0.02386994 | - | - |


## Incident Timeline

| Metric | Value |
|--------|-------|
| Total Events | 624419 |
| Swaps | 248515 |
| Liquidity Events | 15450 |
| Block Range | 24996372 → 25878650 |
| Time Range | 2026-05-01 00:00:59 UTC → 2026-08-31 23:49:11 UTC |

### Liquidity Migration Detected

The following migration candidates were found:
- From [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24996415) to [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24996415)
- From [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24996626) to [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24996626)
- From [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24996932) to [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24996932)
- From [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24996979) to [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24996979)
- From [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24997012) to [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) (block 24997012)

### Alternative Cause Check

- Large token distributions detected — possible airdrop or coordinated sell.

### Key Events by Block

| Block | Timestamp | Event | Pool | Actor | Detail |
|-------|-----------|-------|------|-------|--------|
| 25878620 | 2026-08-31 23:43:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Value: 74925000000.00 |
| 25878620 | 2026-08-31 23:43:11 UTC | SWAP (dex.trades) | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Amount0: 2.5500 |
| 25878620 | 2026-08-31 23:43:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Value: 2.5500 |
| 25878620 | 2026-08-31 23:43:11 UTC | SWAP (dex.trades) | [0xda43c52f...425a2c](https://etherscan.io/address/0xda43c52f98f5062aa46c3e01cb8aaa50ed5aa2e59ee59bbf1882cfce0e425a2c) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Amount0: 150124170000.00 |
| 25878620 | 2026-08-31 23:43:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Value: 150124170000.00 |
| 25878622 | 2026-08-31 23:43:35 UTC | SWAP (dex.trades) | [0xda43c52f...425a2c](https://etherscan.io/address/0xda43c52f98f5062aa46c3e01cb8aaa50ed5aa2e59ee59bbf1882cfce0e425a2c) | [0x8A29F890...3C9425](https://etherscan.io/address/0x8A29F8905B30dECe481f312D3cBb39f29D3C9425) | Amount0: 6.00 |
| 25878622 | 2026-08-31 23:43:35 UTC | SWAP (dex.trades) | [0xe05147bb...459519](https://etherscan.io/address/0xe05147bbe9d8dad6e9e0a9a61daf322c4839dc9a7422850fed19829d5f459519) | [0x6beAc0dd...70a415](https://etherscan.io/address/0x6beAc0dd77044A9B6D290efC8Fb95D1fd670a415) | Amount0: 21821211664.39 |
| 25878622 | 2026-08-31 23:43:35 UTC | SWAP (dex.trades) | [0x259d3ac6...9850ee](https://etherscan.io/address/0x259d3ac6dc6d22ac5aebdba55ba32bf3bcc5dd62b954d4873b2cd562259850ee) | [0x196C00C1...a3eE77](https://etherscan.io/address/0x196C00C1b00000000000007c00739AD9Faa3eE77) | Amount0: 903703703.70 |
| 25878622 | 2026-08-31 23:43:35 UTC | SWAP (dex.trades) | [0x5c8ae631...6396e8](https://etherscan.io/address/0x5c8ae63113f673a5c3d60815d53e772fe39098eb386481c4c654b921a36396e8) | [0x009A8DBa...881b57](https://etherscan.io/address/0x009A8DBaD7000f0000009b002d050058CA881b57) | Amount0: 8150230066.98 |
| 25878649 | 2026-08-31 23:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x52512Aa9...2Aa09b](https://etherscan.io/address/0x52512Aa9785B9Ec16c8BF6767b477aEcAE2Aa09b) | Value: 7.2855 |
| 25878649 | 2026-08-31 23:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xD7185c48...44091F](https://etherscan.io/address/0xD7185c486dD88eb9F3573B878a1469485644091F) | Value: 7.2855 |
| 25878649 | 2026-08-31 23:48:59 UTC | SWAP (dex.trades) | [0xe7e394a4...c35a85](https://etherscan.io/address/0xe7e394a49ecc14872b8c9d46c08a3f3f11f260a7551cca4f603756990bc35a85) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Amount0: 727817159851.44 |
| 25878649 | 2026-08-31 23:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Value: 727817159851.44 |
| 25878649 | 2026-08-31 23:48:59 UTC | SWAP (dex.trades) | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Amount0: 6.0107 |
| 25878649 | 2026-08-31 23:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Value: 6.0107 |
| 25878649 | 2026-08-31 23:48:59 UTC | SWAP (dex.trades) | [0xda43c52f...425a2c](https://etherscan.io/address/0xda43c52f98f5062aa46c3e01cb8aaa50ed5aa2e59ee59bbf1882cfce0e425a2c) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Amount0: 546907167302.92 |
| 25878649 | 2026-08-31 23:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x0889e932...502c9A](https://etherscan.io/address/0x0889e9327b98D7d1BE3C301A4585ff3330502c9A) | Value: 546907167302.92 |
| 25878649 | 2026-08-31 23:48:59 UTC | SWAP (dex.trades) | [0xe05147bb...459519](https://etherscan.io/address/0xe05147bbe9d8dad6e9e0a9a61daf322c4839dc9a7422850fed19829d5f459519) | [0xAe9a7427...17dEAC](https://etherscan.io/address/0xAe9a742713d9dA2655c9F27279d8Ba3d7e17dEAC) | Amount0: 64795803310.62 |
| 25878649 | 2026-08-31 23:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000000...E08A90](https://etherscan.io/address/0x000000000004444c5dc75cB358380D2e3dE08A90) | Value: 16194902.10 |
| 25878649 | 2026-08-31 23:48:59 UTC | SWAP (dex.trades) | [0x94af2942...66a000](https://etherscan.io/address/0x94af294207a2c592c08a39c82a7df42a18613d986eeb520b7164fe9ccd66a000) | [0x6beAc0dd...70a415](https://etherscan.io/address/0x6beAc0dd77044A9B6D290efC8Fb95D1fd670a415) | Amount0: 6985576488.96 |
| 25878649 | 2026-08-31 23:48:59 UTC | SWAP (dex.trades) | [0xda43c52f...425a2c](https://etherscan.io/address/0xda43c52f98f5062aa46c3e01cb8aaa50ed5aa2e59ee59bbf1882cfce0e425a2c) | [0xcCE53ecB...65CdeD](https://etherscan.io/address/0xcCE53ecB8fF3aDEbA49289B5bfBDB6422965CdeD) | Amount0: 14.43 |
| 25878649 | 2026-08-31 23:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000000...E08A90](https://etherscan.io/address/0x000000000004444c5dc75cB358380D2e3dE08A90) | Value: 54913276660.18 |
| 25878649 | 2026-08-31 23:48:59 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0xcCE53ecB...65CdeD](https://etherscan.io/address/0xcCE53ecB8fF3aDEbA49289B5bfBDB6422965CdeD) | Value: 54913276660.18 |
| 25878649 | 2026-08-31 23:48:59 UTC | SWAP (dex.trades) | [0xdc893995...ab0775](https://etherscan.io/address/0xdc893995d488e5be8ec8ca1db92cbec2a1ab0775) | [0xcCE53ecB...65CdeD](https://etherscan.io/address/0xcCE53ecB8fF3aDEbA49289B5bfBDB6422965CdeD) | Amount0: 54913276660.18 |
| 25878650 | 2026-08-31 23:49:11 UTC | SWAP (dex.trades) | [0xda43c52f...425a2c](https://etherscan.io/address/0xda43c52f98f5062aa46c3e01cb8aaa50ed5aa2e59ee59bbf1882cfce0e425a2c) | [0x81463B0f...5b5128](https://etherscan.io/address/0x81463B0f960f247f704377661ec81C1fd65b5128) | Amount0: 10.44 |
| 25878650 | 2026-08-31 23:49:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x00000000...E08A90](https://etherscan.io/address/0x000000000004444c5dc75cB358380D2e3dE08A90) | Value: 39552109776.29 |
| 25878650 | 2026-08-31 23:49:11 UTC | SWAP (dex.trades) | [0x259d3ac6...9850ee](https://etherscan.io/address/0x259d3ac6dc6d22ac5aebdba55ba32bf3bcc5dd62b954d4873b2cd562259850ee) | [0x81463B0f...5b5128](https://etherscan.io/address/0x81463B0f960f247f704377661ec81C1fd65b5128) | Amount0: 39552109776.29 |
| 25878650 | 2026-08-31 23:49:11 UTC | TOKEN_TRANSFER (Transfer) | [N/A...N/A](https://etherscan.io/address/N/A) | [0x81463B0f...5b5128](https://etherscan.io/address/0x81463B0f960f247f704377661ec81C1fd65b5128) | Value: 39552109776.29 |
| 25878650 | 2026-08-31 23:49:11 UTC | SWAP (dex.trades) | [0xda43c52f...425a2c](https://etherscan.io/address/0xda43c52f98f5062aa46c3e01cb8aaa50ed5aa2e59ee59bbf1882cfce0e425a2c) | [0x18F96764...2DC8BF](https://etherscan.io/address/0x18F96764c0785767e794F82E89b8B34F922DC8BF) | Amount0: 4.44 |
| 25878650 | 2026-08-31 23:49:11 UTC | SWAP (dex.trades) | [0x5c8ae631...6396e8](https://etherscan.io/address/0x5c8ae63113f673a5c3d60815d53e772fe39098eb386481c4c654b921a36396e8) | [0x6beAc0dd...70a415](https://etherscan.io/address/0x6beAc0dd77044A9B6D290efC8Fb95D1fd670a415) | Amount0: 16799054524.27 |


## Risk Feature Breakdown

| Feature | Value | Weight | Contribution | Description |
|---------|-------|--------|-------------|-------------|
| Pool Concentration | 0.9948 | 0.15 | 0.1492 | Main pool holds 99.48% of total DEX liquidity. |
| Lp Concentration | 0.0000 | 0.15 | 0.0000 | Largest LP holds 0.00% of pool shares. |
| Withdrawal Severity | 1.0000 | 0.20 | 0.2000 | Liquidity removed is 100.00% of reference TVL. |
| Temporal Proximity | 0.4500 | 0.15 | 0.0675 | No incident block — 7025 liquidity removals in window. |
| Role Sensitivity | 0.0000 | 0.15 | 0.0000 | Deployer unknown — role sensitivity not scored. |
| Market Impact | 0.0000 | 0.15 | 0.0000 | No incident block — market impact requires a crash reference. |
| Combined Activity | 1.0000 | 0.05 | 0.0500 | Suspicious activity: 7025 withdrawals and large sells detected. |
| **Raw Score** | | | **0.4667** | |

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



## Partial refresh coverage

May reused local cache; June-August RPC for 106 verified Uniswap pools and all target-token Transfers. Existing other-DEX swaps retained. LP beneficial-owner history is incomplete; V4 amounts are prior-price estimates.

Provisional: cached May coverage is not revalidated; LP identity incomplete; V4 tail principal amounts estimated from prior pool price. Holdings snapshots were retained.
