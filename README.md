# Spiele: Praxisseminar (Digitale) Spiele in der Sozialen Arbeit, WiSe 2026/27

Twine-Spiele der Teilnehmenden, als Twee-Quellen aufbereitet.

## Struktur

| Ordner | Inhalt |
|---|---|
| `repos/` | Originale GitHub-Repos der Teilnehmenden (unveraendert) |
| `src/<Spiel>/` | Twee-Quelle plus die Bilder, die das Spiel einbindet |
| `build/<Spiel>/` | Gebautes, spielbares HTML plus Bilder (generiert) |
| `formatbau/` | Lehrbeispiel fuer ein eigenes Story-Format (Quelle) |
| `storyformats/` | Projektlokale Story-Formate fuer tweego (generiert aus `formatbau/`) |
| `include/` | frei fuer gemeinsam genutzte Dateien |
| `tools/` | Hilfsskripte |

## Befehle

```bash
# alle Spiele aus src/ nach build/ bauen (-c leert build/ vorher)
tools/build-all.sh -c

# Twine-HTML nach Twee 3 umwandeln
python3 tools/html2twee.py repos/<repo>/index.html src/<Spiel>/<Spiel>.twee

# Miniformat neu verpacken und Beispiel bauen
python3 formatbau/build.py
tweego -o formatbau/beispiel.html formatbau/beispiel.twee
```

Voraussetzungen: `tweego` in `~/go/bin`. Die benoetigten Story-Formate (Harlowe 3.3.9,
Trialogue 0.1.1) liegen in `storyformats/`, tweego findet sie beim Start aus dem
Projektordner.

## GitHub Pages

`.github/workflows/pages.yml` baut bei jedem Push auf `main`, der `src/`,
`storyformats/` oder `tools/` aendert, alle Spiele, erzeugt mit
`tools/make-index.py` eine Startseite `build/index.html` und veroeffentlicht
`build/` auf GitHub Pages. Einmalig im Repo einstellen: Settings -> Pages ->
Source: "GitHub Actions".

## Spiele

| Spiel | Repo | Format |
|---|---|---|
| Wald | qo203/Wald | Harlowe 3.3.9 |
| Der Mann auf den Stufen | sammyibm/Twine | Harlowe 3.3.9 |
| John und die Papiere (+ Version 2) | marcksm04-sketch/John | Harlowe 3.3.9 |
| Die Bibliothek | S910111/Die-Bibliothek | Harlowe 3.3.9 |
| Das Mehl weg ist | friedi0603/index | Harlowe 3.3.9 |
| Der Mann auf den Stufen (Chat) | Umbau von sammyibm/Twine | Trialogue 0.1.1 |
| Trialogue-Demo | phivk/trialogue (`docs/trialogue-demo.twee`) | Trialogue 0.1.1 |

Trialogue (https://github.com/phivk/trialogue) liegt als Format in
`~/.storyformats/trialogue-0.1.1/`. Jede Passage braucht einen Tag `speaker-<name>`,
Links werden zu Antwort-Buttons. Bootstrap und jQuery laedt das Format aus dem Netz,
die Spiele brauchen also eine Internetverbindung.
