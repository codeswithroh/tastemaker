#!/usr/bin/env bash
# Review/approve/reject sponsor submissions.
#
# Setup once: export TASTEMAKER_ADMIN_TOKEN="<the token printed when this
# worker was first deployed — also saved to /tmp/tastemaker_admin_token.txt
# on the machine that set it up>"
#
# Usage:
#   ./admin.sh pending                 list submissions awaiting review
#   ./admin.sh approve <sponsor-id>    put them live in the next open slot
#   ./admin.sh reject <sponsor-id>     decline (soft — row is kept, not deleted)

set -euo pipefail

API="https://tastemaker-sponsors-api.codeswithroh.workers.dev"
TOKEN="${TASTEMAKER_ADMIN_TOKEN:?Set TASTEMAKER_ADMIN_TOKEN first}"

cmd="${1:-}"
case "$cmd" in
  pending)
    curl -s "$API/api/sponsors/pending" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
    ;;
  approve)
    id="${2:?Usage: ./admin.sh approve <sponsor-id>}"
    curl -s -X PATCH "$API/api/sponsors/$id/approve" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
    ;;
  reject)
    id="${2:?Usage: ./admin.sh reject <sponsor-id>}"
    curl -s -X PATCH "$API/api/sponsors/$id/reject" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
    ;;
  *)
    echo "Usage: ./admin.sh {pending|approve <id>|reject <id>}" >&2
    exit 1
    ;;
esac
