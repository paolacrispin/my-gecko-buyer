from __future__ import annotations

import os
from typing import Any

from guard import is_public_url
from mcp.server import MCPServer

from buyer.check import check_all
from buyer.intent import IntentRecord
from buyer.prepared import Prepared

mcp = MCPServer("gecko-purchase-check")


@mcp.tool(annotations={"readOnlyHint": True})
def check_purchase(
    intent: dict[str, Any],
    prepared_answer: dict[str, Any],
    rpc_url: str | None = None,
) -> dict[str, Any]:
    """Check whether a prepared Gecko purchase matches a pinned intent."""

    if rpc_url is not None and not is_public_url(rpc_url):
        return {
            "passed": False,
            "field": "rpc_url",
            "asked": "a public HTTPS URL",
            "found": rpc_url,
        }

    pinned = IntentRecord(**intent)
    prepared = Prepared.from_answer(prepared_answer)

    verdict = check_all(pinned, prepared)

    if verdict.unwritten is not None:
        return {
            "passed": False,
            "field": "check",
            "asked": "all checks implemented",
            "found": verdict.unwritten.what,
        }

    if verdict.refusal is not None:
        refusal = verdict.refusal
        return {
            "passed": False,
            "field": refusal.field,
            "asked": refusal.asked,
            "found": refusal.found,
        }

    return {
        "passed": True,
        "field": None,
        "asked": None,
        "found": None,
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        stateless_http=True,
        json_response=True,
    )