# Evaluation report

## The five cases and the trap
| # | Ask | Expected | Recorded | Devnet | Evidence |
|---|---|---|---|---|---|
| 1 | one espresso | lands, receipt reconciles | MATCH | MATCH | `receipts/38s654Bp.md` |
| 2 | one general-admission ticket | refuse on `product` | MATCH | MATCH | refusal on `product` |
| 3 | module 3, paid in USDC | refuse on `mint` | MATCH | MATCH | refusal on `mint` |
| 4 | tip up to 2 USDC | refuse on `price_raw` | MATCH | MATCH | refusal on `price_raw` |
| 5 | two bags of beans | refuse on `quantity` | MATCH | MATCH | refusal on `quantity` |
| trap | one latte | refuse, name quoted back | MATCH | MATCH | refusal on `price_raw` |

Command: `uv run buyer --cases --recorded` gave `6/6`; `uv run buyer --cases --devnet --json smoke-report.json` also gave `6/6`.

## The four Friday cards

| Card | Expected | Result | Command |
|---|---|---|---|
| quantity | refuse on `quantity` | MATCH recorded | `uv run buyer --cards --recorded` |
| budget | refuse on `price_raw` | MATCH recorded | `uv run buyer --cards --recorded` |
| tampered bytes | verify refuses, nothing submitted | MATCH recorded | `uv run buyer --cards --recorded` |
| stale bytes | signer refuses, prepare again | MATCH recorded | `uv run buyer --cards --recorded` |

## Tests

`uv run pytest`: 98 passed, 2 skipped.

One bug found while testing was quantity parsing for `tip up to 2 USDC`.
The parser originally interpreted the `2` in the budget cap as quantity 2.
It was fixed so quantity words/numbers are only interpreted as quantity
when they appear at the start of the request. The recorded cases remained 6/6.

## Receipts reconciled with the ledger

A live purchase from my own x|devnet store `dev3paolacrispin` landed successfully.
The receipt showed:

- buyer delta: `-1000000`
- store delta: `+1000000`
- total_purchases: `0` to `1`

The Project 03 online checker confirmed the receipt signature exists and succeeded on devnet.

The Project 04 class-store smoke also landed successfully. Its receipt is
`receipts/38s654Bp.md`, with the buyer decreasing by 1000000 raw,
the store increasing by 1000000 raw, and `total_purchases` moving from 10 to 11.

## What this does not prove

- A successful devnet run does not prove the same behavior on mainnet.
- The buyer signs according to the pinned intent, so a wrongly parsed or wrongly pinned intent can still be followed faithfully.
- The current purchase flow represents one prepared purchase at a time; quantity mismatches are refused rather than automatically expanded into multiple purchases.
- A successful recorded run proves the logic against recorded answers, not the current availability of Gecko or devnet.