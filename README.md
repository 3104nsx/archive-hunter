
# archive-hunter

Turn-key, Dockerized Python 3.11 project that continuously scans EU & JP fashion resale platforms, filters by curated archive/avant-garde brands (with aliases), deduplicates, and posts finds to Discord.

## v1 Providers
- **eBay** (HTML via lxml/cssselect)
- **Vinted** (JSON API)
- Stubs (disabled): Vestiaire Collective, Grailed, Mercari JP, Buyee/Yahoo Auctions

## Services (docker compose)
- `hunter-eu`, `hunter-jp` — main engine reading `config.eu.yaml` / `config.jp.yaml`
- `dashboard` — FastAPI `/health` → `{"ok": true}`
- `metrics` — FastAPI `/metrics` → `ok\n`
- `backlog`, `burst` — stubs
- `discord-bot` — stub exits 0 if token missing

## Quickstart (Windows & Ubuntu)
1. Copy `.env.example` to `.env`, set `DISCORD_WEBHOOK_DEFAULT` (or region-specific).
2. `docker compose build`
3. `docker compose up -d`
4. Visit http://localhost:8090/health and http://localhost:9108/metrics

### Sanity checks
```bash
docker compose exec -T hunter-eu python tools/self_test.py    # "imports OK"
docker compose exec -T hunter-eu python finder_opt.py --dry-run --once --provider ebay --brand "Rick Owens"
```

## Strict .dockerignore
Deny-all with explicit whitelist to avoid uploading host folders or `.env` into the image.

## Repo Tree
(see repository files)

## Hetzner CCX13 (prod overlay)
- Use `docker-compose.prod.yml` to remove ports; access via SSH tunnels.
- Example tunnels:
  ```bash
  ssh -N -L 8090:localhost:8090 ubuntu@SERVER_IP
  ssh -N -L 9108:localhost:9108 ubuntu@SERVER_IP
  ```

## Troubleshooting
- **.env not found**: ensure it sits next to `docker-compose.yml`.
- **Windows Access is denied / WinSAT**: strict `.dockerignore` prevents huge contexts.
- **PowerShell blocked**: run `Set-ExecutionPolicy -Scope Process Bypass -Force` (session-only).
- **No Discord posts**: verify webhook; try `--dry-run`; check `docker logs -f hunter-eu`.
- **403/429**: cadence + jitter help; consider cookies later.
- **Network timeouts**: retries via providers; engine never crashes.
- **YAML errors**: validated by `tools/self_test.py`.

## Future Enhancements
- SQLite for `seen.json`
- Deals channel, quiet hours backlog digest
- Provider cookies / Playwright storage state
- S3/R2 backups of `data/` by retention
- Exporter JSONL/CSV
- Prometheus counters, histograms

## Security
- Keep secrets in `.env`
- Respect site ToS
- UTF-8 files, newline at EOF; pinned `requirements.txt`

## 60-Second Checklist
1) Copy `.env.example` → `.env`, paste webhook  
2) `docker compose build`  
3) `docker compose up -d`  
4) `docker compose ps` + `docker logs -f hunter-eu`  
5) `/health` → `{"ok": true}`; `/metrics` → `ok\n`  
6) (Optional) dry-run eBay once
