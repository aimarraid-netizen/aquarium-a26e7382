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

- `F[name]` — kala objekt (`base`, `skin`, `morph`, `homeY`…); `cum[name]` kumulatiivsed punktid; `sizeOf(v)` eksponentskaala.
- **Kalaliigid:** `fishSVG(n,idx,species,bucket,metal)` + `speciesShape(sp)` — 6 parameetrilist SVG-keha (piraaja/hai/ahven/karp/räim/mõõkkala), viewBox `-14 0 92 48`, keha tsenter ~(34,24). Baasliik idx-st, **esikolmik koha järgi** (`TOP3`=3× hai, eristub metalli järgi kuld/hõbe/pronks). Custom-art (`fish/shark.svg`) laetakse `CUSTOM`-i; metallkalal tulevad uimed+heledus metalli toonist. `skin`-cache → `body.innerHTML` uueneb AINULT liigi/ilme/metalli muutudes (jõudlus).
- **Saba = riigilipp:** `flagStops(code)` ehitab vertikaalse gradiendi (horisontaalsed triibud); `FCODE` (EE/PL/**PLEE**=Ola&Kaur). 4-täheline kood = jagatud saba (ülemine pool = 1. riik).
- **Morfoloogia:** `morph=rank/(N-1)` → `bucket` (ilme: silm/suu) + loop'is keha-droop-rotate + `el.style.filter` kahvatus. Tipp uhke/sirge, põhi longus/kahvatu/kurb.
- `applyStep(i,eat)` — seis + liigi/morph-uuendus; `triggerFeed(i)` — **lihatükk** kukub, punkti saajad rebivad tüki (`tearPiece`, 2p suurem), `spawnParticles` (pool `PCL`) + `flashTank`.
- `celebrateOlle(i)` — Olle 2-punkti eriefekt (9.4s, ajatelg pausile via `tick` `if(celebrating)return`). `finale()` — võitja koroneerimine i===LAST.
- Edetabel reastub ümber; `.boss` (kuld-glow) 1. kohale. Kommentaator + tempo-valik EEMALDATUD (vt Lõksud).
- **Keel (et/pl):** `LANG` = `?lang=pl|et` > `localStorage.aq_lang` > brauseri keel (`pl*`→pl, muidu et). `I18N.et/.pl` → `T`;
  staatilised tekstid seatakse DOM-i kohe pärast `DATA` laadimist, nupp `#lang` vahetab keelt (salvestab + laeb URL-iga uuesti).
  Riiginimed: `TEAM_PL` + `TEAM_RE` (pikimad ees) → `plTeams()` rakendub PL-režiimis `matchLabels[].m`-ile. Sheet jääb inglise keelde.

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
- **Auto-täisekraan on brauseris VÕIMATU** (requestFullscreen nõuab kasutaja klõpsu). Leht avaneb **tavavaates** (mitte enam pseudo-fullscreenis); `⛶ Täisekraan`-nupp annab päris Fullscreen API ja kukub vajadusel tagasi CSS-pseudo-fullscreeni (`fs-fallback`, täidab ekraani, pealkirjad peidus). Ära lisa load'il requestFullscreen ega `fs-fallback`-i — kasutaja valib ise.
- Jõudlus: per-frame'is EI tohi panna CSS `filter`-it kõigile kaladele (kahvatus käib `applyStep`-is, harva). Boids/screenshake teadlikult välja jäetud (v2). Particle'id pool'itud (`PCL`).

## Ajalugu

- 29.06.2026: loodud `~/Downloads/wc2026_aquarium.html`-ist; lisatud dashboardile (`:8080/aquarium/`).
- 29.06.2026: DATA → `data.json` (Google Sheetist), GitHub Pages deploy, cron-automaatika 15 min.
  Transform verifitseeritud: genereeritud data.json = käsitsi-sisestatud DATA (kõik 9 välja identsed).
- 29.06.2026: suur visuaalne ümbertegemine (4-disaineri töövoog → süntees → jõudluskriitik): kalaliigid,
  esikolmik (kuld-piraaja/hõbe-hai/pronks-kiskja), saba-lipud, söögi-rebimine, caustic/sügavus/finaal;
  eemaldatud kommentaator + tempo-valik.
- 29.06.2026: ujumis-süsteem ümber (boids-lite eraldumine, dart&glide hoog, sujuv kursipööre, saba vehib kiirusega,
  kallutus üles/alla); esikolmik = 3× hai (custom `fish/shark.svg`, metall kuld/hõbe/pronks); surnud-räimed kõht ülespidi;
  **medali number `.mnum`-grupis, loop keerab vasakule ujudes `scale(-1,1)` → number jääb õigetpidi mõlemas suunas.**

- 20.07.2026: poolakeelne versioon — i18n samas failis (`?lang=pl`, keelenupp, riiginimed poola keeles).

> Seotud: `~/projects/worldcup-bot/` (sama Sheet + ennustusmäng, botikomponent).
