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

## Koht → liik (mootor valib automaatselt)

| Failid | Roll | Kuju (sina teed) | Mootor lisab |
|---|---|---|---|
| `piranha.svg` `shark.svg` `perch.svg` | top 3 röövkalad | kuri/ülbe röövkala hammastega | kuld/hõbe/pronks + kroon(1)/medal(2,3) |
| `carp.svg` `sword.svg` | keskmik | tavaline sõbralik kala | mängija värv |
| `deadfish.svg` | põhi 3 | kidur surnud räim, X-silmad | keerab KÕHT ÜLESPIDI, kahvatuks |

**Art on KOHA-NEUTRAALNE** — ära joonista krooni, medalit ega keera kala ümber. Mootor teeb seda koha järgi (koht muutub animatsiooni ajal).

## Promtid (kopeeri-kleebi)

**RÖÖVKALAD** (jooksuta 3×, vaheta liik: PIRAAJA / HAI / OGALINE AHVEN-KISKJA):
```
Tee mulle ÜKS akvaariumi-kala SVG, liik: PIRAAJA — kuri, ülbe röövkala.
- viewBox="-14 0 92 48", vaatab PAREMALE, läbipaistev taust, keskel.
- Turske keha, ettetorkav alalõug suurte valgete (#fff) kolmnurksete hammastega, vihane silm+kulm. Korralik, mitte räbal-koomiks.
- ÄRA lisa krooni ega medalit.
- Placeholder-värvid (kasuta TÄPSELT, ainult nendel osadel — ma asendan koodis):
    keha = lapik täide #8FB3B8 · saba = #3C6CA8 · muud uimed/tumedad = #2F5358 · kõht-hele = #D6E6E6
- Silm valge #fff + must #0a1a26 ~(54,20). Kontuur #1d2e30. Neid värve mujal ära kasuta.
- Saba mähi: <g class="tw" style="transform-box:view-box;transform-origin:16px 24px">…</g>
- Väljund: AINULT puhas SVG-kood.
```

**SÕBRALIKUD** (jooksuta 2×: KARPKALA / MÕÕKKALA-pika-ninaga):
```
Tee mulle ÜKS akvaariumi-kala SVG, liik: KARPKALA — tavaline sõbralik rahulik kala.
- viewBox="-14 0 92 48", vaatab PAREMALE, läbipaistev taust, keskel. Lihtne, sõbralik, "normaalne".
- Placeholder-värvid (TÄPSELT): keha #8FB3B8 · saba #3C6CA8 · uimed #2F5358 · kõht #D6E6E6
- Silm valge #fff + must #0a1a26 ~(54,20), sõbralik. Kontuur #1d2e30.
- Saba: <g class="tw" style="transform-box:view-box;transform-origin:16px 24px">…</g>
- Väljund: AINULT SVG.
```

**SURNUD RÄIM** (1×):
```
Tee mulle ÜKS akvaariumi-kala SVG, liik: SURNUD RÄIM — kidur, pooleldi surnud.
- viewBox="-14 0 92 48", vaatab PAREMALE, joonista PÜSTI (mootor keerab ise kõht ülespidi), läbipaistev taust.
- Kõhn luine haletsusväärne keha; nähtavad roided; X-kujulised surnud silmad (mustad #0a1a26 jooned); lõtv avatud suu.
- Placeholder-värvid (TÄPSELT): keha #8FB3B8 · saba #3C6CA8 · uimed #2F5358 · kõht #D6E6E6
- Saba: <g class="tw" style="transform-box:view-box;transform-origin:16px 24px">…</g>
- Väljund: AINULT SVG.
```

Salvesta iga tulemus õige nimega (`piranha.svg` jne) ja lae filebrowseriga siia kausta. Faili lisamisel asendub see kala kohe.
