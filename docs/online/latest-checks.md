# Latest application checks

Checked October 8, 2026 (Korea time).

- Frontend production build: PASS (TypeScript and Vite).
- Backend regression suite: PASS, 15 tests across order/payment, owner management, and Trash.
- Public browser check: PASS; app loads, monthly order folders display, White/Dark/Code themes work, appearance survives reload, and owner dashboard opens without browser exceptions.
- Trash tests cover restore, permanent deletion, 30-day expiry, and paid-order protection.
- Sales tests cover Korea-time daily boundaries. Daily totals include all paid orders in the shared database, including sample purchases.

[Latest interface screenshot](latest-ui.png). [Earlier simulated checkout result](verification.json) and [checkout screenshot](public-check.png) record the previous complete payment verification; they are historical evidence, not a new purchase today.

## Run checks

From smartserve-pos:

```powershell
docker compose -p smartserve-week5-check exec -T api python -m unittest -v test_issue3 test_owner_management test_trash
docker compose -p smartserve-week5-check exec -T web npm run build
```

Payments are simulated. The public link requires the host PC, Docker services, proxy, and tunnel to remain running. Automated checks do not replace a teammate's independent setup and review.
