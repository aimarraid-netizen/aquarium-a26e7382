#!/usr/bin/env python3
"""Lae MM 2026 ennustusmängu Google Sheet ja genereeri data.json akvaariumi jaoks.

Allikas: avalik (link-ligipääsetav) Google Sheet, eksporditud xlsx-na.
Tab "Matches-results-bets-points" sisaldab kõike: mängud, tulemused, igaühe bett + punktid,
championi-pakkumised (rida "World champion (5 pts)"). Punktid on sheetis ETTE arvutatud.

Ainult standardteek (urllib, zipfile, xml) — sama lähenemine kui worldcup-bot/bot.py.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

SHEET_ID = "1XN_oDXDhUP-upHVr3m4mldv7OPHFmbck"
XLSX_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"
SHEET_TAB = "Matches-results-bets-points"
OUT = Path(__file__).resolve().parent / "data.json"
TALLINN = ZoneInfo("Europe/Tallinn")

# Teadaolevad trükivead sheetis (allika autori sisestus) → parandus kuvamiseks.
TEAM_TYPO_FIX = {"Hailti - Scotland": "Haiti - Scotland"}

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RELNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def download_xlsx() -> bytes:
    req = urllib.request.Request(XLSX_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    if not data.startswith(b"PK"):
        raise RuntimeError("Google Sheet export ei tagastanud xlsx/zip faili (ligipääs?)")
    return data


def _colnum(ref: str) -> tuple[int, int]:
    m = re.match(r"([A-Z]+)(\d+)", ref)
    col = 0
    for ch in m.group(1):
        col = col * 26 + (ord(ch) - 64)
    return int(m.group(2)), col


def read_cells(xlsx_bytes: bytes, tab: str) -> dict[tuple[int, int], str]:
    z = zipfile.ZipFile(__import__("io").BytesIO(xlsx_bytes))
    shared: list[str] = []
    try:
        sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in sst.iter(NS + "si"):
            shared.append("".join(t.text or "" for t in si.iter(NS + "t")))
    except KeyError:
        pass
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    relmap = {r.get("Id"): r.get("Target") for r in rels}
    target = None
    for s in wb.iter(NS + "sheet"):
        if s.get("name") == tab:
            t = relmap[s.get(RELNS + "id")]
            target = t if t.startswith("xl/") else "xl/" + t
    if target is None:
        raise RuntimeError(f"Tabi ei leitud: {tab}")
    root = ET.fromstring(z.read(target))
    cells: dict[tuple[int, int], str] = {}
    for c in root.iter(NS + "c"):
        ref, t = c.get("r"), c.get("t")
        v, isn = c.find(NS + "v"), c.find(NS + "is")
        val = ""
        if v is not None and v.text is not None:
            val = shared[int(v.text)] if t == "s" else v.text
        elif isn is not None:
            val = "".join(x.text or "" for x in isn.iter(NS + "t"))
        if val != "":
            cells[_colnum(ref)] = val
    return cells


def norm_score(s: str) -> str:
    """'2 : 0' -> '2:0' ; 'x 1 : 1' -> 'x 1:1' ; '' -> ''."""
    if not s:
        return ""
    return re.sub(r"\s*:\s*", ":", s.strip())


def build() -> dict:
    cells = read_cells(download_xlsx(), SHEET_TAB)
    maxr = max(r for r, _ in cells)
    maxc = max(c for _, c in cells)

    # Päis (rida 1): leia mängijad — veerg, mille järel on 'pts' veerg.
    FIXED = {"time", "match", "result", "pts", ""}
    players: list[tuple[str, int, int]] = []  # (nimi, betcol, ptscol)
    for c in range(1, maxc + 1):
        name = cells.get((1, c), "").strip()
        nxt = cells.get((1, c + 1), "").strip().lower()
        if name and name.lower() not in FIXED and nxt == "pts":
            players.append((name, c, c + 1))
    if not players:
        raise RuntimeError("Mängijaid ei leitud päisest")

    match_col = next(c for c in range(1, maxc + 1) if cells.get((1, c), "").strip().lower() == "match")
    date_col = match_col - 2  # A=date, B=time, C=match
    result_col = match_col + 1

    # Champion-rida
    champ_row = None
    for r in range(2, maxr + 1):
        if cells.get((r, match_col), "").lower().startswith("world champion"):
            champ_row = r
            break

    names = [p[0] for p in players]
    matchLabels, ptsByPlayer, betsByPlayer = [], {n: [] for n in names}, {n: [] for n in names}
    last_date = ""
    for r in range(2, (champ_row or maxr + 1)):
        teams = re.sub(r"\s+", " ", cells.get((r, match_col), "").strip())
        if cells.get((r, date_col)):
            last_date = cells[(r, date_col)].strip()
        if not teams or " - " not in teams:
            continue  # vahe- või kokkuvõtte-rida
        result = norm_score(cells.get((r, result_col), ""))
        if not result:
            continue  # veel mängimata (nt tulevased knockout-mängud) — ilmub kui tulemus tuleb
        teams = TEAM_TYPO_FIX.get(teams, teams)
        matchLabels.append({"m": teams, "d": last_date, "r": result})
        for name, bc, pc in players:
            betsByPlayer[name].append(norm_score(cells.get((r, bc), "")))
            pv = cells.get((r, pc), "")
            ptsByPlayer[name].append(float(pv) if pv else 0.0)

    champ = {}
    if champ_row:
        for name, bc, _ in players:
            champ[name] = cells.get((champ_row, bc), "").strip()

    total = {n: sum(ptsByPlayer[n]) for n in names}
    exact = {n: sum(1 for p in ptsByPlayer[n] if p == 2.0) for n in names}
    correct = {n: sum(1 for p in ptsByPlayer[n] if p >= 1.0) for n in names}

    return {
        "names": names,
        "matchLabels": matchLabels,
        "ptsByPlayer": ptsByPlayer,
        "betsByPlayer": betsByPlayer,
        "total": total,
        "exact": exact,
        "correct": correct,
        "champ": champ,
        "nMatches": len(matchLabels),
        "updatedAt": datetime.datetime.now(TALLINN).isoformat(timespec="seconds"),
    }


def main() -> int:
    data = build()
    # updatedAt muutub iga käivitusega — et cron ei push'iks asjata, säilita vana tempel
    # kui sisuline andmestik on identne (timestamp näitab siis "viimati MUUTUS", mitte "viimati laeti").
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding="utf-8"))
            if {k: v for k, v in data.items() if k != "updatedAt"} == {
                k: v for k, v in old.items() if k != "updatedAt"
            }:
                data["updatedAt"] = old.get("updatedAt", data["updatedAt"])
        except (json.JSONDecodeError, OSError):
            pass
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"data.json: {data['nMatches']} mängu, {len(data['names'])} mängijat, uuendatud {data['updatedAt']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
