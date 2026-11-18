---
status: shipped
test: `python3 docs/features/2026-11-18-gallery-industries/check.py all`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()"`
commits: b469c4348f1ee6bfcab4a76c1741d1ed48990afd..e8f2f6d60bb97eaf1901abdade5771210b5176f2
---

# Gallery industry list (`INDUSTRIES`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the `site-generator` component and the playbook (spec Scope, `Design: none`).
Every command runs from the repository root. The checks live in `check.py` next to this file.
`check.py all` runs every check except `browser`, with no network and no browser.
`check.py browser` drives the installed Google Chrome through Playwright. It serves the repository on a
free local port itself and blocks every request that does not go to that port.
`check.py` is approved together with this file. Changing what it checks goes back to a person for re-approval.

- [x] T1 Replace `INDUSTRIES` in `scripts/profiles.py` with the nine industries (AC1) — verify: `python3 docs/features/2026-11-18-gallery-industries/check.py data`
- [x] T2 Replace the gallery `desc` string in `scripts/build.py` with the string in spec AC12, then regenerate the pages with `python3 scripts/build.py` (AC2·AC3·AC4·AC5·AC6·AC7·AC8·AC9·AC10·AC11·AC12·AC13) — verify: `python3 scripts/build.py >/dev/null && python3 docs/features/2026-11-18-gallery-industries/check.py gallery`
- [x] T3 Check the chip filter on `/profile/` in a browser: each of the nine chips shows exactly its industry's cards, or its one 준비 중 tile (AC14) — verify(browser): `python3 docs/features/2026-11-18-gallery-industries/check.py browser`
- [x] T4 Update `docs/profile-playbook.md`: the §3 업종 key line lists the nine keys in order (AC15). Add one bullet or paragraph that holds the words `fitness`, `beauty`, `프랜차이즈`, `매장 찾기` and `가맹 문의` (AC16). Add one bullet or paragraph that holds the words `law`, `invest`, `crypto`, `광고`, `AC` and `clinic` (AC17) (AC15·AC16·AC17) — verify: `python3 docs/features/2026-11-18-gallery-industries/check.py playbook`
- [x] T5 Keep the branch inside its scope (AC18·AC19) — verify: `python3 docs/features/2026-11-18-gallery-industries/check.py scope`

Always last, never removed:

- [x] T6 Reconcile `docs/current_system/` with what shipped, and set `last_reconciled` in `overview.md` to the new HEAD (AC20·AC21) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-18-gallery-industries/check.py current`
