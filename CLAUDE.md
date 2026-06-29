# aquarium — MM 2026 Ennustusakvaarium 🐟

Sõpruskonna jalgpalli-ennustusmängu (MM 2026) edetabel **akvaariumina**: iga osaleja on kala,
mis kasvab punktide võrra. Üksik isemajandav HTML-visualiseering — kogu CSS, JS ja andmed ühes failis.

## Käivitamine

```bash
# Lihtsalt ava brauseris:
xdg-open ~/projects/aquarium/index.html
```
Väline sõltuvus: ainult Google Fonts (Oswald, Inter, JetBrains Mono). Muu CDN-vaba, töötab offline (fondid puuduvad).

## Arhitektuur

- **Üks fail** `index.html` — kogu CSS + JS + andmed sees. Hoia ühes failis (artefakti-stiil), kui pole teisiti palutud.
- **Andmed**: `const DATA = {...}` script-tagi alguses. Väljad:
  - `names` (16 mängijat), `matchLabels` (m/d/r = match/date/result), `ptsByPlayer`, `betsByPlayer`,
    `total`, `exact`, `correct`, `champ`, `nMatches` (73 mängu — alagrupid).
- **Animatsioon**: `requestAnimationFrame` loop. Kalad on DOM-divid (SVG keha), liiguvad
  virtuaalkoordinaadistikus VW=900 × VH=560, skaleeritud `sx`/`sy`-ga.

## Põhimõisted koodis

- `F[name]` — kala objekt (`x,y,vx,vy,size,target,seek,flee,orbit,flip…`).
- `cum[name]` — kumulatiivsed punktid mängude kaupa; `sizeOf(v)` = eksponentskaala.
- `applyStep(i, eat)` — renderda seis mängu *i* järel; `eat=true` → söötmise FX.
- `triggerFeed(i)` — söök kukub; punkti saajad ujuvad kohale (`seek`), nulli saajad eemale (`flee`).
- `celebrateOlle(i)` — eriefekt Olle ainsa 2-punkti hetkel (mäng 55).
- Edetabel paremal reastub ümber; kroon/medal 1.–3. kohale.
- Täisekraan: avaneb pseudo-fullscreenis (`fs-fallback` klass); nupp annab päris Fullscreen API (vajab klõpsu).

## Stiil

- Värvid: `--gold #ffd54a` (liider), `--teal`, dark turf akvaarium.
- Mängijate värvid `PAL` massiivis + SVG mustrid (triibud/täpid) `fishSVG()`-s.
- Lipud: SVG (EE sinine-must-valge, PL valge-punane), `flagHTML()`. `FCODE` = mängija → lipukood (EE/PL/EEPL).
- **UI ja kommentaator eesti keeles** — säilita.

## Lõksud

- Andmed elavad koodis (`DATA`-konstant). Excelist uuendamiseks tuleb `DATA`-blokk käsitsi asendada.
- `betsByPlayer` on ainult kuvamiseks; punktiarvestus käib `ptsByPlayer`-ist (eelarvutatud).
- **`x` viigi ees/järel EI ole viga.** Väljalangemismängudes tuleb viigi ennustamise korral märkida
  ka lõppvõitja: `x1:1` = võidab vasakpoolne (esimene) meeskond, `1:1x` = võidab parempoolne (teine).
  Nt `betsByPlayer["Magda & Krzysiek"]` mäng 73 = `"x 1:1"` on kehtiv sisestus, mitte trükiviga.

## Edasiarendus (kui asjakohane)

- Tõsta `DATA` eraldi `data.json`-i ja lae `fetch()`-iga (lihtsam Excelist uuendada).
- Säilita kood ühes failis, kui pole teisiti palutud.

## Ajalugu

- Loodud `~/Downloads/wc2026_aquarium.html`-ist projektiks 29.06.2026.
- Parandatud 1 andmeviga: `"Hailti - Scotland"` → `"Haiti - Scotland"` (mäng 7, kuvamis-tasandil).
  (`"x 1:1"` jäi alles — vt Lõksud, see on kehtiv väljalangemis-märge, mitte viga.)

> Seotud: `~/projects/worldcup-bot/` (sama MM 2026 ennustusmängu botikomponent).
