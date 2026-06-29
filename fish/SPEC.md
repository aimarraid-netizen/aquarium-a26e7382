# Kala-SVG spetsifikatsioon (`fish/`)

Pane siia kausta oma kala-SVG-d. Mootor laeb need automaatselt ja asendab sisseehitatud kala.
Failinimi = liik: **`piranha.svg`, `shark.svg`, `perch.svg`, `carp.svg`, `herring.svg`, `sword.svg`**.
Faili puudumisel kasutatakse sisseehitatud kala (miski ei katki). Vt malli: [`_example.svg`](_example.svg).

## Reeglid

1. **Külgvaade, nina PAREMALE.** Läbipaistev taust.
2. **viewBox** soovituslikult `"-14 0 92 48"` (sama kui mall) — siis on saba, silm ja kroon õiges kohas.
   Muu viewBox töötab ka, aga hoia kala lõuendil keskel, nina paremal, saba vasakul.
3. **Placeholder-värvid** — kasuta TÄPSELT neid HEX-koode AINULT värvitavatel osadel (mootor asendab):
   | Värv | Osa | Millega mootor asendab |
   |---|---|---|
   | `#8FB3B8` | **keha** põhipind (lapik täide, ära pane gradienti) | mängija värv / metall (#1 kuld, #2 hõbe, #3 pronks) |
   | `#3C6CA8` | **saba** uim | riigi lipuvärv (gradient-triibud) |
   | `#2F5358` | muud **uimed / tumedad** aktsendid | tume varjund kehavärvist |
   | `#D6E6E6` | **kõhu-hele** | hele varjund kehavärvist |
   Kõik muu (silm `#fff`/`#0a1a26`, hambad `#fff`, kontuur `#1d2e30` jms) jääb **fikseeritud** — neid ära kasuta värvitavatel osadel.
4. **Saba mähi `<g class="tw" style="transform-box:view-box;transform-origin:Xpx Ypx">…</g>`** kus X,Y = saba liigend (mall: 16,24). Siis saba vehib.
5. **Ära lisa** krooni/medaleid — mootor lisab #1-le krooni ise.

## Prompt Claude designile (kopeeri-kleebi, vaheta KALA välja)

```
Tee mulle ÜKS akvaariumi-kala SVG, liik: PIRAAJA.
Nõuded:
- viewBox="-14 0 92 48", kala vaatab PAREMALE, läbipaistev taust, keskel lõuendil.
- Korralik, "normaalse" välimusega külgvaade (mitte koomiks-räbal). Selge siluett ka väiksena.
- Kasuta TÄPSELT neid placeholder-värve ainult nendel osadel (ma asendan need koodis):
    keha põhipind = lapik täide #8FB3B8 (ära pane kehale gradienti)
    saba uim = #3C6CA8
    muud uimed / tumedad jooned = #2F5358
    kõhu-hele = #D6E6E6
- Silm: valge #fff + must #0a1a26 pupill, ~(54,20). Suu/kontuur tume #1d2e30. Need värvid ära mujal kasuta.
- Mähi saba <g class="tw" style="transform-box:view-box;transform-origin:16px 24px"> sisse.
- Piraajal: turske sügav keha, ettetorkav alalõug suurte valgete (#fff) kolmnurksete hammastega, vihane silm.
- Väljund: AINULT puhas SVG-kood, ilma seletuseta.
```

Salvesta tulemus nimega `piranha.svg` siia kausta (filebrowseri kaudu). Korda iga liigi jaoks.
