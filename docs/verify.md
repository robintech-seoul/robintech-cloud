# Repository-wide verification

Applies to every feature in this repository.

- [ ] Generated pages are in sync with the generator and data — verify: `python3 scripts/build.py >/dev/null && git diff --quiet -- index.html 404.html cases privacy profile/index.html`
- [ ] Generator scripts parse — verify: `python3 -m py_compile scripts/build.py scripts/cases.py scripts/profiles.py scripts/profile_thumb.py`
- [ ] Shared JS parses — verify: `node --check assets/js/main.js`
