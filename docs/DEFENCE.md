# The defence: Friday 2 October, six minutes

*Your script. Keep the minutes, fill the right-hand column with what YOU will show and
say, and rehearse it once on Thursday against the clock. Delete the italic lines.*

One design rule: everything you show ends in a **receipt** (it landed, and this is what
moved) or a **refusal** (it did not sign, and this is the field that disagreed).

## The six minutes
| Min | On screen | Backed by | What I say |
|---|---|---|---|
| 0:00 | my README's first lines and the devnet explorer link | `README.md` | My capstone is a buyer agent that either pays exactly what I asked for or refuses and names the field that disagreed. The important rule is that no transaction is signed until the prepared bytes have been checked against a pinned intent. |
| 0:45 | Gecko `list_stores` showing `dev3paolacrispin` | `docs/connect.md`, `store/store.json` | This is my store on Solana devnet. Gecko can read its three products, but Gecko never holds my private key. My keys stay outside the repository in `~/.config/dev3pack/`. |
| 1:30 | `uv run buyer "one espresso" --devnet` | live buyer run | Here the request is pinned before any transaction exists. Gecko prepares unsigned bytes, my buyer checks program, store, product, price, mint, quantity and destination, then signs, verifies the signed bytes and only then submits. |
| 2:30 | the devnet explorer and the reconciled receipt | `receipts/<sig8>.md` | I do not treat a successful submit response as proof. The receipt reads the ledger before and after. In my live purchase the buyer moved -1000000, the store moved +1000000, and total_purchases moved from 0 to 1. |
| 3:15 | one injected failure card and its refusal | `buyer/check.py`, `refusals/` | A refusal is also a successful outcome. For example, asking for two units when Gecko prepared one refuses on quantity before signing. Tampered signed bytes are rejected by verify before submit, and stale bytes are rejected before signing. |
| 4:30 | tests, recorded cases and evaluation report | `uv run pytest`, `docs/EVAL_REPORT.md` | My tests currently pass with 98 passed and 2 skipped. The recorded cases are 6/6 and the four failure cards are 4/4. Testing also exposed a real parser bug: the 2 in “tip up to 2 USDC” was initially interpreted as quantity, so I changed quantity parsing and reran the suite. |
| 5:15 | the ADR about refusing before signing | `docs/adr/0001-refusals-before-signing.md` | My design decision is to compare every safety-relevant field before signing and verify the signed bytes again before submission. I would remove a check only if I could demonstrate that another independently enforced guarantee binds the same property without weakening the refusal boundary. |
The **finalists** (the students presenting on Friday, named by the instructor) may do
minute 1:30 on mainnet against geckocoffee instead, with a registered, funded wallet (see
"Friday on mainnet" below). Everyone else stays on devnet, and that is the whole defence.

**If the network or Gecko is down on stage,** switch to the recorded answers and say so:
`GECKO_SOURCE=recorded uv run buyer "one espresso" --devnet`. Same code path, replayed.

## The four cards

The judge draws one, face down. You do not know which, so you cannot stage it; your
buyer has to refuse it on its own.

| Card | What the judge does | The command | The expected refusal |
|---|---|---|---|
| **Quantity** | asks for two espressos | `uv run buyer "two espressos" --devnet` | `quantity`: asked 2, prepared 1 |
| **Budget** | sets the budget to half the price | `uv run buyer "one espresso" --budget-raw <half> --devnet` | `price_raw`: both numbers |
| **Tampered bytes** | changes one byte of the signed transaction before verify | `uv run buyer "one espresso" --devnet --card tampered` | `signed bytes`: `verify_signed_transaction` refuses, so there is no submit |
| **Stale bytes** | waits past `expires`, then asks you to sign | `uv run buyer "one espresso" --devnet --card stale` | `blockhash`: the bytes expired; prepare again, never re-sign |

**Stale takes about 40 seconds live:** the runner waits on the chain until the bytes
expire. Say what it is waiting for while it waits. Measured on devnet on 30 September:
quantity and budget 3 s, tampered 8 s, stale 41 s.

Rehearse all four offline first, with no network and no key:

```bash
uv run buyer --cards --recorded                        # 4/4 once your steps and checks are written
uv run buyer "one espresso" --recorded --card tampered # one card at a time
```

## The notebook version

`demo/DEMO_DAY.ipynb` is these six minutes as one cell per beat: your README, `list_stores`,
the live buy, the receipt, the card (set `CARD` to the one drawn), tests, the ADR, and the
mainnet and recorded lanes. Open it with:

```bash
uv run --with jupyter jupyter lab demo/DEMO_DAY.ipynb
```

Run it once on Thursday and keep the outputs: if the network fails on stage, the notebook
that already ran is your fallback, and you say that is what it is.

## Before you go on stage

- [ ] One devnet receipt is **committed** (`receipts/<sig8>.md`). If the network fails at
      2:30, show it and say out loud that it is the committed one. Same code path, honest.
- [ ] `uv run buyer --cases --recorded` prints 6/6 and `--cards` prints 4/4.
- [ ] `uv run pytest` is green and `python3 scripts/scan_secrets.py` finds nothing.
- [ ] Your devnet buyer holds SOL and your token (`solana balance -u devnet <buyer>`).
- [ ] Your assistant's connector is live; you tried `list_stores` today, not yesterday.
- [ ] Mainnet only: `uv run python scripts/mainnet_wallet.py show` prints 300000 raw USDC
      and some SOL, and `mainnet-wallet.json` is not in `git status`.

## Friday on mainnet (your own wallet, registered and funded)

The key is made on your machine and never leaves it. Do steps 1 to 5 before Friday.

1. **Make the wallet, on your own machine.**

   ```bash
   uv run python scripts/mainnet_wallet.py create
   ```

   It writes `~/.config/dev3pack/mainnet-wallet.json` (mode 600, outside this repository)
   and prints the public address only. It refuses to overwrite a wallet that exists.

2. **Get a Gecko key**, with the Gecko CLI (published on PyPI as `gecko-surf`; `uvx` runs it
   without installing anything):

   **Finalists: your instructor sends you a Gecko key privately, already granted.** Skip
   to step 4 and paste it at the prompt (it is not echoed). Otherwise:

   ```bash
   uvx --from gecko-surf gecko login --email <you@example.com>
   ```

   It emails you a one-time code and seals the key in your OS keychain. Where there is no
   keychain (WSL2, a headless Linux box), it shows the key once instead: copy it then.

3. **Tell the instructor the email you logged in with.** Your Gecko account is that email,
   and the instructor grants it to the class. Until then, `register` answers `not-granted`.

4. **Register the wallet's address.** Put the key in `GECKO_API_KEY` without it ever
   appearing on screen, or leave it unset and paste it at the prompt (not echoed):

   ```bash
   export GECKO_API_KEY="$(uvx keyring get gecko:gecko-identity gecko)"
   uv run python scripts/mainnet_wallet.py register
   ```

   It fetches a one-time challenge, signs it with the wallet, and sends the address and the
   signature. The key file never leaves your machine; the Gecko key is never printed. It
   prints `registered <address> for <account>`, or Gecko's reason, word for word.
   Each run uses a fresh one-time challenge; if it fails, fix the reason and run it once
   more (on `rate-limited`, wait a minute first; never loop it). Registering a different
   address **replaces** the old one, which may already be funded: it warns you, stops
   until you pass `--replace`, and either way you tell the instructor.

5. **Wait for funding, then check it.**

   ```bash
   uv run python scripts/mainnet_wallet.py show
   ```

   The founder funds each registered address with 300000 raw USDC (three espressos at
   100000) and about 0.0094 SOL for fees. `show` reads both from a public mainnet RPC and
   signs nothing.

6. **Friday: the buy.**

   ```bash
   uv run buyer "one espresso" --mainnet --store geckocoffee
   ```

   The mainnet lane reads only that wallet, pays in mainnet USDC, and caps every signature
   at `--mainnet-budget-raw 300000` by default. The signer refuses a cap above 300000, any
   purchase above the cap, and any node whose genesis hash is not mainnet's.

**Mainnet is real money.** The budget is the cap, and the balance is the hard one: a
fourth espresso cannot be paid for. Never share the key file, never commit it, never
paste it anywhere (the pre-commit scan refuses `mainnet-*.json`, but that is a seatbelt).
The wallet signs two things only: the registration challenge, and Friday's purchases.
No PayBox, no hosted signer: the key is yours and stays on your machine. Telegram is an
optional extra channel, once a transaction has worked from the terminal.

On stage, run `show` first so the room sees three espressos' worth of USDC, then the buy,
then `show` again: the USDC went down by exactly the price.

## The seven questions you will be asked

The same list is on the course's session 15 page. Have each answer ready with a file
attached.

**The evidence**

1. **How do you know it landed?** Not "the terminal said so". The receipt: two ledger
   reads, the deltas, `total_purchases` going from n to n+1, and the explorer link.
2. **What does your receipt not prove?** It proves what moved. It cannot prove that you
   asked for the right thing. Have the limit ready in `docs/ISSUES.md`.
3. **Your buyer refused. How does the person at the chat know it was right to?** The
   refusal names one field and both values, and `refusals/<stamp>-<field>.json` keeps it.

**The design**

4. **Why does Gecko never hold your key, and what would change if it did?** Know where
   your key lives, and which step in `buyer/signer.py` uses it.
5. **Which of your seven checks would you drop first, and what risk would you accept?**
   Answer from `buyer/check.py`, field by field.
6. **What would change your mind about your ADR?** The measurement that would reverse
   it. If nothing would, it was a preference, not a decision.

**The limits**

7. **What breaks it?** You already know one thing. Say it before the card makes it
   obvious.
