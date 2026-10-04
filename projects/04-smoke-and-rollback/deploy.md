# Check server deployment

## Public MCP endpoint

My `check_purchase` MCP server is deployed on Render using Streamable HTTP:

https://my-gecko-buyer.onrender.com/mcp

The server is keyless. It checks prepared purchases but never loads a signer or private key.

## Live check_purchase call

I called the deployed server with the recorded `two bags of beans` case.

The server exposed:

```text
TOOLS: ['check_purchase']
```

The `check_purchase` result was:

```text
{'passed': False, 'field': 'quantity', 'asked': 2, 'found': 1}
```

This is the expected refusal: the pinned intent asked for two bags of beans, while the prepared transaction contained one purchase.

## SSRF guard

I also called `check_purchase` with:

```text
rpc_url = http://127.0.0.1:8899
```

The deployed server refused it before any network fetch:

```text
{'passed': False, 'field': 'rpc_url', 'asked': 'a public HTTPS URL', 'found': 'http://127.0.0.1:8899'}
```

This confirms that the public deployment still refuses private or non-HTTPS RPC destinations.

## Redeploy

The service is connected to the `main` branch of:

```text
paolacrispin/my-gecko-buyer
```

Pushing a new commit to `main` redeploys the service on Render. I can also use Render's manual "Deploy latest commit" action.

The start command is:

```bash
uv run python server/check_server.py
```

## Rollback

If the deployed server, Gecko, or devnet is unavailable during the defence, I switch to the recorded lane:

```bash
GECKO_SOURCE=recorded uv run buyer --cases --json smoke-report.recorded.json
```

The recorded rollback currently gives `6/6` using the same buyer checks without network access, a key, or token movement.