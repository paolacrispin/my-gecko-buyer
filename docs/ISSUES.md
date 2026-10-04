# Issues

## 2026-10-04: Live smoke could not prepare purchases because the buyer had no class tokens

- **What I saw:** running `uv run buyer --cases --devnet --json smoke-report.json` produced `Gecko refused, receipt-failed` for the live purchases. The message said that the buyer's `sender_token_account` for the class-store mint did not exist on devnet. The smoke finished with `0/6 cases match what the fixtures expect`.
- **What was actually wrong:** my devnet buyer had SOL and my own token, but it did not yet hold the class tokens used by `dev3pack-cafe`. In particular, the smoke needs the class mint `Eoqdd43nFQ9HzGq8HjBRVLCV6aTqCFRiwHy1ZVQheYSi` and the lookalike mint `BRPT4Sr7CWcJhfdwMJektzvLFKjgzVBK2AfrW4nPCEM6`.
- **How I found it:** Gecko's simulation error explicitly identified the missing `sender_token_account`. I compared that with the successful purchase from my own store, where the buyer already held my own token.
- **What I changed:** no signing or transaction code needed to change. I requested the required class tokens for my buyer and kept using the recorded lane while waiting. I will rerun the same live smoke command after the tokens arrive.
- **What it cost:** no tokens were spent and nothing was signed or submitted. The failure happened during `prepare`, before signing.
- **Would the checks have caught it?** No. The seven checks compare a successfully prepared transaction with the pinned intent. Here Gecko could not produce a transaction at all because the buyer lacked the token account, so the simulation refused before the checks.