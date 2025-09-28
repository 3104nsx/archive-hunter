
import os, sys
token = os.environ.get("DISCORD_BOT_TOKEN")
if not token:
    print("[discord-bot] no token; exiting 0")
    sys.exit(0)
# Minimal placeholder to keep container healthy if token exists (no real bot loop yet)
print("[discord-bot] token present; placeholder exiting 0 for v1")
sys.exit(0)
