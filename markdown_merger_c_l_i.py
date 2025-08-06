#!/usr/bin/env python3
"""
MD-Merger - Ein CLI-Tool zum Zusammenfügen von Markdown-Dateien
"""

import os
import argparse
import sys
from pathlib import Path
from typing import List, Union

def collect_md_files_from_directory(directory: str) -> List[str]:
    """
    Sammelt rekursiv alle .md Dateien aus einem Verzeichnis.
    
    Args:
        directory: Pfad zum Verzeichnis
        
    Returns:
        Liste der Markdown-Dateipfade, sortiert nach ASCII-Codes
    """
    md_files = []
    
    for root, dirs, files in os.walk(directory):
        # Sortiere Verzeichnisse nach ASCII-Codes
        dirs.sort()
        
        for file in sorted(files):  # Sortiere Dateien nach ASCII-Codes
            if file.lower().endswith('.md'):
                full_path = os.path.join(root, file)
                md_files.append(full_path)
    
    return md_files

def read_markdown_file(filepath: str) -> str:
    """
    Liest eine Markdown-Datei und gibt den Inhalt zurück.
    
    Args:
        filepath: Pfad zur Markdown-Datei
        
    Returns:
        Inhalt der Datei als String
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Fehler: Datei '{filepath}' nicht gefunden.", file=sys.stderr)
        return ""
    except UnicodeDecodeError:
        print(f"Fehler: Datei '{filepath}' konnte nicht als UTF-8 gelesen werden.", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Fehler beim Lesen der Datei '{filepath}': {e}", file=sys.stderr)
        return ""

def merge_markdown_files(files: List[str], output_file: str, add_separators: bool = True) -> bool:
    """
    Fügt mehrere Markdown-Dateien zu einer zusammen.
    
    Args:
        files: Liste der Eingabedateien
        output_file: Pfad zur Ausgabedatei
        add_separators: Ob Trennlinien zwischen Dateien hinzugefügt werden sollen
        
    Returns:
        True bei Erfolg, False bei Fehler
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            for i, filepath in enumerate(files):
                print(f"Verarbeite: {filepath}")
                
                content = read_markdown_file(filepath)
                if not content:
                    continue
                
                # Füge Header mit Dateinamen hinzu
                filename = os.path.basename(filepath)
                output.write(f"<!-- Quelle: {filepath} -->\n\n")
                
                # Schreibe Dateiinhalt
                output.write(content)
                
                # Stelle sicher, dass Datei mit Zeilenumbruch endet
                if not content.endswith('\n'):
                    output.write('\n')
                
                # Füge Trenner hinzu (außer bei der letzten Datei)
                if add_separators and i < len(files) - 1:
                    output.write('\n---\n\n')
        
        return True
    
    except Exception as e:
        print(f"Fehler beim Schreiben der Ausgabedatei '{output_file}': {e}", file=sys.stderr)
        return False

def validate_input_files(files: List[str]) -> List[str]:
    """
    Validiert und filtert Eingabedateien.
    
    Args:
        files: Liste der zu validierenden Dateipfade
        
    Returns:
        Liste der gültigen Markdown-Dateien, sortiert nach ASCII-Codes
    """
    valid_files = []
    
    for file in files:
        if not os.path.exists(file):
            print(f"Warnung: Datei '{file}' existiert nicht und wird übersprungen.", file=sys.stderr)
            continue
        
        if not os.path.isfile(file):
            print(f"Warnung: '{file}' ist keine Datei und wird übersprungen.", file=sys.stderr)
            continue
        
        if not file.lower().endswith('.md'):
            print(f"Warnung: '{file}' ist keine Markdown-Datei und wird übersprungen.", file=sys.stderr)
            continue
        
        valid_files.append(file)
    
    # Sortiere nach ASCII-Codes
    return sorted(valid_files)

def main():
    """Hauptfunktion des CLI-Tools."""
    
    parser = argparse.ArgumentParser(
        description='Fügt Markdown-Dateien zu einer einzigen Datei zusammen.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Beispiele:
  %(prog)s -f datei1.md datei2.md -o zusammengefuegt.md
  %(prog)s -d ./docs -o alle_docs.md
  %(prog)s -f *.md -o output.md --no-separators
        '''
    )
    
    # Eingabe-Optionen (sich gegenseitig ausschließend)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-f', '--files',
        nargs='+',
        help='Liste der Markdown-Dateien zum Zusammenfügen (mindestens 2)'
    )
    input_group.add_argument(
        '-d', '--directory',
        help='Verzeichnis zum rekursiven Sammeln aller Markdown-Dateien'
    )
    
    # Ausgabe-Optionen
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Pfad zur Ausgabedatei'
    )
    
    # Weitere Optionen
    parser.add_argument(
        '--no-separators',
        action='store_true',
        help='Keine Trennlinien zwischen Dateien einfügen'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Überschreibe Ausgabedatei ohne Nachfrage'
    )
    
    args = parser.parse_args()
    
    # Sammle Eingabedateien
    if args.files:
        if len(args.files) < 2:
            print("Fehler: Mindestens zwei Dateien müssen angegeben werden.", file=sys.stderr)
            sys.exit(1)
        
        input_files = validate_input_files(args.files)
    else:
        if not os.path.exists(args.directory):
            print(f"Fehler: Verzeichnis '{args.directory}' existiert nicht.", file=sys.stderr)
            sys.exit(1)
        
        if not os.path.isdir(args.directory):
            print(f"Fehler: '{args.directory}' ist kein Verzeichnis.", file=sys.stderr)
            sys.exit(1)
        
        input_files = collect_md_files_from_directory(args.directory)
        input_files = validate_input_files(input_files)
    
    # Prüfe, ob Eingabedateien gefunden wurden
    if not input_files:
        print("Fehler: Keine gültigen Markdown-Dateien gefunden.", file=sys.stderr)
        sys.exit(1)
    
    if len(input_files) < 2:
        print("Fehler: Mindestens zwei gültige Markdown-Dateien sind erforderlich.", file=sys.stderr)
        sys.exit(1)
    
    # Prüfe Ausgabedatei
    if os.path.exists(args.output) and not args.force:
        response = input(f"Ausgabedatei '{args.output}' existiert bereits. Überschreiben? (j/N): ")
        if response.lower() not in ['j', 'ja', 'y', 'yes']:
            print("Abgebrochen.")
            sys.exit(0)
    
    # Zeige Zusammenfassung
    print(f"Gefundene Dateien ({len(input_files)}):")
    for file in input_files:
        print(f"  - {file}")
    print(f"\nAusgabe: {args.output}")
    print()
    
    # Führe Zusammenfügung durch
    success = merge_markdown_files(
        input_files, 
        args.output, 
        add_separators=not args.no_separators
    )
    
    if success:
        print(f"\nErfolgreich! {len(input_files)} Dateien wurden zu '{args.output}' zusammengefügt.")
        
        # Zeige Statistiken
        output_size = os.path.getsize(args.output)
        print(f"Größe der Ausgabedatei: {output_size:,} Bytes")
    else:
        print("\nFehler beim Zusammenfügen der Dateien.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
