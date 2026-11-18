---
status: shipped
approved_at: e8f2f6d60bb97eaf1901abdade5771210b5176f2
commits: b469c4348f1ee6bfcab4a76c1741d1ed48990afd..e8f2f6d60bb97eaf1901abdade5771210b5176f2
---

# Gallery industry list (`INDUSTRIES`)

## Problem

A marketing partner recommended the homepage profile types RobinTech should sell: 법무법인, 병원,
필라테스 (franchise), 미용실 (franchise), 인테리어, 코인 and 투자자문 (private equity). The `/profile/`
gallery still offers the old industry list. It shows filter chips and "준비 중" tiles for 키즈 · 교육,
숙박 · 공간대여 and 전문 서비스, which RobinTech no longer targets. It has no chip for 법무법인, 인테리어,
코인 or 투자자문. A visitor who opens the gallery sees industries RobinTech does not plan to build. Sales
cannot point a law firm, an interior studio, a crypto business or an investment adviser to their own industry.
The gallery meta description also names 키즈카페. The playbook's industry key list, which sample builders
follow, lists the old keys.

## Scope

"The nine industries" below means these `(key, label)` pairs, in this order:
`law` 법무법인, `clinic` 병원 · 의원, `fitness` 필라테스, `beauty` 미용실, `interior` 인테리어,
`crypto` 코인 · 가상자산, `invest` 투자자문, `food` 식당 · 카페, `flower` 꽃집 · 공방.
"The old labels" means 전문 서비스, 키즈 · 교육, 숙박 · 공간대여, 운동 · 피트니스 and 뷰티 · 미용.
"The five samples" means `food-saebyeokmil`, `flower-bomgyeol`, `clinic-neuru`, `clinic-byeotteul` and `clinic-bonui`.

- **In:** Replace `INDUSTRIES` in `scripts/profiles.py` with the nine industries (AC1).
- **In:** Remove 키즈카페 from the gallery meta description in `scripts/build.py` (AC12, AC13).
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py` (AC2–AC14).
- **In:** Update the industry key list in `docs/profile-playbook.md` §3 to the nine keys (AC15).
- **In:** A short playbook note on what fitness and beauty samples are and on advertising-rule ACs for law, invest and crypto (AC16, AC17).
- **In:** Reconcile `docs/current_system/` and set `last_reconciled` (AC20, AC21).
- **Out:** Building any new sample, including samples for the six new or renamed industries with no sample.
- **Out:** Changes to the five sample folders, to `assets/`, and to any other part of `scripts/build.py`.
- **Out:** Aliases or redirects for the removed keys `kids`, `stay` and `pro`.
- **Out:** The gallery hero and lead copy ("우리 가게에 …"), `AGENTS.md` §8, the gallery Esc behaviour in `assets/js/main.js`, and `profile-queue.md`.
- **Design:** none. Trigger 1 (crosses a component boundary): no. Only `site-generator` data and the copy it emits change; `site-assets` and `profile-samples` are untouched. Trigger 2 (adds a component): no. Trigger 3 (alters a named interface): no. `INDUSTRIES` keeps its shape `list[tuple[key, label]]` (overview) and its contract (filter chip order; a live profile whose `industry` is not listed stops the build, `site-generator/component.md`); only its values change, and every `industry` in `PROFILES` (food, flower, clinic) stays listed. Trigger 4 (adds a module boundary): no. So `spec.md` + `tasks.md` is enough.

## Acceptance criteria

Data

- [ ] AC1 `INDUSTRIES` in `scripts/profiles.py` equals the nine industries, exactly and in order.

Generated gallery (`profile/index.html`)

- [ ] AC2 `python3 scripts/build.py` exits 0.
- [ ] AC3 The filter chips in `profile/index.html` are `all` followed by the nine keys, in order.
- [ ] AC4 Each industry filter chip shows the label of its key from the nine industries.
- [ ] AC5 The `all` chip shows the count `5`.
- [ ] AC6 The `clinic` chip shows the count `3`, and the `food` and `flower` chips show the count `1`.
- [ ] AC7 The `law`, `fitness`, `beauty`, `interior`, `crypto` and `invest` chips show no count.
- [ ] AC8 `profile/index.html` has exactly six "준비 중" tiles, one each for `law`, `fitness`, `beauty`, `interior`, `crypto` and `invest`.
- [ ] AC9 No `data-filter` or `data-industry` attribute in `profile/index.html` has the value `kids`, `stay` or `pro`.
- [ ] AC10 `profile/index.html` contains none of the old labels.
- [ ] AC11 `profile/index.html` has one card for each of the five samples, with the same `data-industry` as on `main`.
- [ ] AC12 The `meta name="description"` content in `profile/index.html` is exactly "꽃집, 식당, 병원 등 업종별로 설계한 로빈테크 홈페이지 디자인 프로파일. 마음에 드는 디자인을 골라 우리 가게 홈페이지로 만들어 보세요.".
- [ ] AC13 The `og:description` content in `profile/index.html` is exactly the AC12 string.
- [ ] AC14 On `/profile/` served from the repository root over local HTTP, clicking each of the nine industry chips shows only that industry's cards or its "준비 중" tile (browser).

Playbook

- [ ] AC15 The 업종 key line in `docs/profile-playbook.md` §3 lists exactly the nine keys, in order, and no other key.
- [ ] AC16 `docs/profile-playbook.md` states that `fitness` and `beauty` samples are franchise brand sites with a store locator and a 가맹 문의 section.
- [ ] AC17 `docs/profile-playbook.md` states that a `law`, `invest` or `crypto` sample's spec researches that industry's advertising rules and turns them into ACs, as the clinic spec did for medical advertising.

Unchanged files

- [ ] AC18 Compared with `main`, the branch changes no file outside `scripts/profiles.py`, `scripts/build.py`, `profile/index.html` and `docs/`.
- [ ] AC19 Compared with `main`, `scripts/build.py` changes only the gallery `desc` string.

Reconciliation

- [ ] AC20 `docs/current_system/` names no removed key (`kids`, `stay`, `pro`) and none of the old labels.
- [ ] AC21 `git diff` from the `last_reconciled` commit in `docs/current_system/overview.md` to `HEAD` shows no change outside `docs/`.

Every AC above is checked by a `tasks.md` verify (command or browser); there is no `verify.md`.

## Assumptions

- The keys, labels and order are the human's decision of 2026-11-18. `pro` is renamed to `law`, not kept beside it. `kids` and `stay` are removed. This change ships as its own PR before any new sample.
- The new gallery `desc` string (AC12) drops 키즈카페 and adds no new copy. Playbook §2 asks for a reason when the gallery part of `build.py` changes: the old string names an industry the gallery no longer has.
- The labels 필라테스 and 미용실 drop the partner's "프랜차이즈". The playbook note of AC16 keeps that intent for the sample builders.
- The playbook note of AC17 names no statute. Each later sample's spec finds and cites the rules for its industry.
- `python3 scripts/build.py` also rewrites `index.html`, `cases/`, `privacy/` and `404.html`. Their data does not change, so they rebuild byte-identical. If T5 reports one of them, the committed page was already stale: stop and ask, do not revert it.
- Removing `kids`, `stay` and `pro` breaks no link. They were chip filters and "준비 중" tiles only, with no URL.
- `docs/current_system/` lists no industry keys or labels today, so AC20 already holds. Reconciliation is expected to change only `last_reconciled`.
- `docs/current_system/` is current: on 2026-11-18 `git diff --stat 6dd13ab..HEAD` lists only docs files (`overview.md` `last_reconciled`, the clinic spec and tasks frontmatter from the SHA re-pointing commit). No code changed, so no reconciliation is needed before tasks.

## Open questions
