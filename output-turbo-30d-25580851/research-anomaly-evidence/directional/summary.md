# Directional Swap Flow Audit

- Pool: `0x7baece5d47f1bc5e1953fbe0e9931d54dab6d810`
- Event window: blocks `25684865`–`25720864`
- Balance snapshots: blocks `25684864` → `25720864`

## Reconciliation

| Metric | TURBO |
|---|---:|
| Sell volume into pool | 16134606.503579624127458096 |
| Buy volume out of pool | 15384439.103717844428077472 |
| Net Swap event flow to pool | 750167.399861779699380624 |
| Actual ERC-20 transfer net to pool | -4515015.383441964848424198 |
| Pool balance delta | -4515015.383441964848424198 |
| Transfer minus Swap | -5265182.783303744547804822 |
| Balance minus Transfer | 0 |

Transfer/balance reconciliation: **exact**.

## Activity

- Swap events: 192 (83 sells / 109 buys)
- Unique Swap transactions: 188
- Unique transaction senders: 0
- Transfer net inside Swap transactions: 750167.399861779699380627 TURBO
- Transfer net outside Swap transactions: -5265182.783303744547804825 TURBO

## Top transaction senders by sell volume

| tx.from | Sell | Buy | Net Swap to pool | Transactions |
|---|---:|---:|---:|---:|
| `unknown` | 16134606.503579624127458096 | 15384439.103717844428077472 | 750167.399861779699380624 | 271 |

## Interpretation guardrail

Swap event amounts describe the pool swap calculation. For a token with custom transfer behavior or other same-window pool movements, they need not equal the ERC-20 balance change. Here, target-token Transfer logs reconcile the historical balance exactly; the non-zero Transfer-minus-Swap residual must be investigated rather than labelled automatically as a fee.
