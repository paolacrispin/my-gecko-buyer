from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlsplit


def is_public_url(url: str) -> bool:
    """Return True only for public HTTPS destinations.

    If a hostname cannot be resolved, refuse it. Failing closed is safer than
    allowing a destination whose network location could not be verified.
    """
    try:
        parsed = urlsplit(url)
    except ValueError:
        return False

    if parsed.scheme != "https":
        return False

    host = parsed.hostname
    if not host:
        return False

    try:
        # Literal IP such as https://8.8.8.8/
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            info = socket.getaddrinfo(host, parsed.port or 443, type=socket.SOCK_STREAM)
        except socket.gaierror:
            return False

        addresses = []
        for entry in info:
            address = entry[4][0]
            try:
                addresses.append(ipaddress.ip_address(address))
            except ValueError:
                return False

    if not addresses:
        return False

    return all(address.is_global for address in addresses)