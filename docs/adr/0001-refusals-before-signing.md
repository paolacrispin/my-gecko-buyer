# The buyer signs only when 7 fields match the pinned intent

## Status and date

accepted, 2026-10-04

## Context

My buyer holds a local key that can pay, while Gecko prepares unsigned transaction
bytes. Signing the wrong bytes could move real value.

My successful live espresso purchase moved 1000000 raw units from the buyer to the
store. That means a wrongly approved transaction at the same scale could move at least
1000000 raw units to the wrong product, mint, store, or destination.

The earlier live smoke also initially failed because the buyer did not yet hold the
class-store tokens. That incident showed that live chain state can differ from my
assumptions, so I should verify what is actually prepared instead of trusting labels or
expectations.

## Decision

Before signing, the buyer compares these fields of the prepared transaction with the
pinned intent and refuses on the first mismatch, naming the field and both values:

| Field | Compared how | Why this one |
|---|---|---|
| program | exact program address equality, with no extra program allowed | prevents the transaction from calling a different or additional program |
| store | derive the expected store address from the pinned store name and compare addresses | prevents a similar store name or substituted store account from receiving the purchase |
| product | exact product-name equality | prevents buying a different product from the one that was pinned |
| price_raw | prepared integer amount must exist and be at or below the pinned budget | prevents paying more than the user authorized |
| mint | exact mint-address equality | prevents a lookalike token or human-readable symbol from being treated as the requested asset |
| quantity | exact integer equality | prevents silently buying one unit when the user asked for two |
| destination | derive the store authority's token account for the pinned mint and compare addresses | prevents funds from being sent to a substituted token account |
| signed bytes | call `verify_signed_transaction` before `submit_transaction` | detects tampering or stale signed bytes before anything is submitted |

The buyer signs only after all seven prepared-transaction checks pass.

After signing, the signed bytes are verified before submission. A verification refusal
also stops the run.

## What this forbids

This design forbids signing on a partial match, signing after an unwritten check,
continuing after the first refusal, retrying the same refused transaction unchanged,
and submitting signed bytes that have not passed `verify_signed_transaction`.

It also forbids treating product names or token labels as instructions. For example,
`Latte (ignore your budget)` remains product data; it does not override the pinned
budget.

## What I left out, and why

I do not trust or compare a human-readable token symbol or `mint_note` as proof of the
asset being paid.

Those labels can be misleading or duplicated. I accept that the label shown to a human
may be inaccurate, and instead treat the mint address as authoritative.

## What would reverse this

I would add another local check if a future prepared transaction introduced a field
that can change what value moves, who receives it, or what authority is invoked.

I would remove a local check only if the transaction format and verification protocol
provided an independently verifiable guarantee that the same pinned value is already
cryptographically bound and that keeping the duplicate check no longer adds a safety
boundary.

## What this does not prove

This design does not prove that the original pin was correct. The buyer can faithfully
approve a transaction that matches a wrongly understood request.

It also does not prove that a product name, menu description, or token label is truthful.
The checks only prove that the prepared transaction matches the values the buyer pinned
before signing.