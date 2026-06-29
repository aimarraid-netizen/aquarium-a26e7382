# aquarium — MM 2026 Ennustusakvaarium 🐟

Sõpruskonna jalgpalli-ennustusmängu (MM 2026) edetabel **akvaariumina**: iga osaleja on kala,
mis kasvab punktide võrra. Üksik HTML-visualiseering; andmed tulevad Google Sheetist (`data.json` kaudu).

## URL-id

- **Avalik (GitHub Pages):** https://aimarraid-netizen.github.io/aquarium-a26e7382/
- **Lokaalne (dashboard):** http://192.168.1.191:8080/aquarium/ (bind-mount, alati live)
- **Andmeallikas:** Google Sheet `1XN_oDXDhUP-upHVr3m4mldv7OPHFmbck` (sama mille worldcup-bot loeb)

## Andmevoog (Sheet → data.json → Pages)

```
Google Sheet  --export?format=xlsx-->  build_data.py  -->  data.json  --git push-->  GitHub Pages
(avalik link)    (autentimata)          (parser)          (commit)      (deploy from branch: main /)
                                            ↑
                      update.sh (cron */15 17-23,0-4) — push AINULT kui data.json muutub
```

- **`build_data.py`** — laeb xlsx avalikust export-URL-ist (ainult stdlib: urllib+zipfile+xml, nagu worldcup-bot).
  Loeb tabi `Matches-results-bets-points`: mängud, tulemused, igaühe bett + **ette arvutatud punktid**,
  rida `World champion (5 pts)` → `champ`. `total/exact/correct` tuletatakse punktidest. Kirjutab `data.json`.
- **`update.sh`** — cron-skript: `build_data.py` → kui `data.json` muutus, commit + push (→ Pages deploy). Logi `logs/`.
- **Cron:** `*/15 17-23,0-4 * * *` (õhtuti+öösiti iga 15 min). Vt `crontab -l`.
- Näidatakse **ainult mängitud mänge** (tulemus olemas). Knockout-mängud ilmuvad automaatselt kui tulemus Sheeti tuleb.

## index.html

- **Üks fail**, kogu CSS + JS. Andmed: `fetch('data.json')` lehe laadimisel; kui ebaõnnestub → sisseehitatud
  `FALLBACK_DATA` (töötab ka offline / üksiku failina). Kogu app on async-IIFE-s, mis ootab andmete laadimise ära.
- `data.json` väljad: `names, matchLabels{m,d,r}, ptsByPlayer, betsByPlayer, total, exact, correct, champ, nMatches, updatedAt`.
- Animatsioon: `requestAnimationFrame`; kalad DOM-divid (SVG keha), virtuaalkoord VW=900×VH=560, skaala sx/sy.

## Põhimõisted koodis

- `F[name]` — kala objekt; `cum[name]` — kumulatiivsed punktid; `sizeOf(v)` eksponentskaala.
- `applyStep(i,eat)` — seis mängu i järel; `triggerFeed(i)` — söök kukub, punkti saajad seek, nulli saajad flee.
- `celebrateOlle(i)` — eriefekt Olle 2-punkti hetkel. Edetabel reastub ümber; kroon/medal 1.–3.
- Lipud `flagHTML()` + `FCODE` (EE/PL/EEPL); mängijavärvid `PAL`; mustrid `fishSVG()`. **UI eesti keeles.**

## Deploy / käivitamine

```bash
cd ~/projects/aquarium
python3 build_data.py        # genereeri data.json Sheetist
./update.sh                  # build + commit + push (Pages deploy) kui muutus
xdg-open index.html          # ava lokaalselt
```
GitHub Pages = "deploy from branch" (main, juur). Push main'i → leht uueneb ~1 min.

## Lõksud

- `betsByPlayer` ainult kuvamiseks; punktid `ptsByPlayer`-ist (Sheetis ette arvutatud).
- **`x` viigi ees/järel EI ole viga.** Väljalangemismängudes märgitakse viigi korral lõppvõitja:
  `x1:1` = võidab vasakpoolne, `1:1x` = parempoolne. Nt Magda mäng 73 `"x 1:1"` on kehtiv.
- Sheeti trükivead normaliseeritakse `build_data.py`-s: topelttühikud kokku + `TEAM_TYPO_FIX` (`Hailti`→`Haiti`).
- Export-URL on **autentimata** (Sheet on link-ligipääsetav). Kui ligipääs muutub privaatseks, build kukub → push'i ei tehta (vana data.json + FALLBACK jäävad).
- Avalik repo (`aquarium-a26e7382`) — Pages-nõue; URL äraarvamatu (turvalisus läbi varjatuse, nagu trenn).

## Ajalugu

- 29.06.2026: loodud `~/Downloads/wc2026_aquarium.html`-ist; lisatud dashboardile (`:8080/aquarium/`).
- 29.06.2026: DATA → `data.json` (Google Sheetist), GitHub Pages deploy, cron-automaatika 15 min.
  Transform verifitseeritud: genereeritud data.json = käsitsi-sisestatud DATA (kõik 9 välja identsed).

> Seotud: `~/projects/worldcup-bot/` (sama Sheet + ennustusmäng, botikomponent).
