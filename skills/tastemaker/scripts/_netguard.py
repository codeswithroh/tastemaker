"""Network egress guard, shared by every fetching script in this skill.

Two jobs:

1. **Scheme allowlist.** `urllib.request.urlopen` honours `file://`, `ftp://`,
   and `data:` as well as HTTP(S). Any script that passes a URL taken from an
   API response straight to `urlopen` can therefore be talked into reading a
   local file by a hostile or compromised record. Everything here is https-only.

2. **Host allowlist.** The skill contacts a small, fixed set of documented
   services. Anything else is refused loudly rather than fetched quietly, so a
   redirect or a poisoned search result cannot pull bytes from an unvetted
   domain.

Both checks are re-applied after redirects, which is where a naive allowlist
usually leaks: the first URL passes, the 302 target does not.
"""

from __future__ import annotations

import urllib.error
import urllib.parse
import urllib.request

# Every host this skill is permitted to contact, and why. Adding to this list
# is a deliberate act: `scripts/check_domains.py` cross-checks it, and any
# domain that appears in docs or code but not here fails the check.
ALLOWED_HOSTS = {
    "api.iconify.design": "icons (Iconify public API, keyless, attribution-free)",
    "api.openverse.org": "photography search (Openverse, keyless, CC0/PDM filtered)",
    "pixabay.com": "optional higher-curation photography (needs PIXABAY_API_KEY)",
    "cdn.jsdelivr.net": "pinned JS library delivery (Motion)",
    "cdnjs.cloudflare.com": "pinned JS library delivery (GSAP + ScrollTrigger)",
}

USER_AGENT = "tastemaker-skill/1.0 (+https://github.com/codeswithroh/tastemaker)"


class BlockedURLError(ValueError):
    """Raised when a URL fails the scheme or host allowlist."""


def _host_allowed(host: str) -> bool:
    host = (host or "").lower().split(":")[0]
    if host in ALLOWED_HOSTS:
        return True
    # Permit subdomains of an allowed host, but never a lookalike that merely
    # ends with the string (e.g. "evil-pixabay.com" must not match).
    return any(host.endswith("." + allowed) for allowed in ALLOWED_HOSTS)


def assert_url_allowed(url: str) -> str:
    parts = urllib.parse.urlparse(url)
    if parts.scheme != "https":
        raise BlockedURLError(
            f"refusing non-https URL (scheme {parts.scheme!r}): {url[:120]}"
        )
    if not _host_allowed(parts.netloc):
        raise BlockedURLError(
            f"refusing URL outside the allowlist (host {parts.netloc!r}): {url[:120]}\n"
            f"Allowed hosts: {', '.join(sorted(ALLOWED_HOSTS))}"
        )
    return url


class _GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-run the allowlist on every redirect target."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        assert_url_allowed(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_opener = urllib.request.build_opener(_GuardedRedirectHandler())


def urlopen_checked(url: str, timeout: int = 25):
    """urlopen with the scheme + host allowlist enforced, redirects included."""
    assert_url_allowed(url)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return _opener.open(req, timeout=timeout)
