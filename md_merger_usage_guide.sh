# Einzelne Dateien zusammenfügen
python md_merger.py -f datei1.md datei2.md datei3.md -o zusammengefuegt.md

# Ganzen Ordner rekursiv durchsuchen
python md_merger.py -d ./docs -o alle_docs.md

# Ohne Trennlinien zwischen Dateien
python md_merger.py -f *.md -o output.md --no-separators

# Bestehende Datei überschreiben
python md_merger.py -d ./markdown-files -o result.md --force
