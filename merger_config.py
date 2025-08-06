#!/usr/bin/env python3
"""
Erweiterte Konfiguration für MD-Merger
"""

import yaml
import json
from typing import Dict, Any, List

class MergerConfig:
    """Konfigurationsklasse für erweiterte Merger-Optionen."""
    
    def __init__(self, config_file: str = None):
        self.config = self._load_default_config()
        
        if config_file:
            self._load_config_file(config_file)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Lädt die Standardkonfiguration."""
        return {
            'output': {
                'encoding': 'utf-8',
                'line_ending': '\n',
                'add_toc': False,
                'add_timestamps': False
            },
            'processing': {
                'skip_empty_files': True,
                'normalize_line_endings': True,
                'remove_duplicate_headers': False
            },
            'separators': {
                'between_files': '---',
                'add_file_headers': True,
                'header_format': '<!-- Quelle: {filepath} -->'
            },
            'filters': {
                'exclude_patterns': ['.git', '__pycache__', '.DS_Store'],
                'include_only': ['.md'],
                'max_file_size_mb': 10
            }
        }
    
    def _load_config_file(self, config_file: str):
        """Lädt Konfiguration aus Datei."""
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    user_config = yaml.safe_load(file)
                elif config_file.endswith('.json'):
                    user_config = json.load(file)
                else:
                    raise ValueError(f"Nicht unterstütztes Konfigurationsformat: {config_file}")
                
                # Merge mit Standardkonfiguration
                self._deep_merge(self.config, user_config)
        
        except Exception as e:
            print(f"Warnung: Konfigurationsdatei konnte nicht geladen werden: {e}")
    
    def _deep_merge(self, base: Dict, update: Dict):
        """Führt Deep-Merge von Konfigurationsdictionarys durch."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Holt Konfigurationswert mit Punkt-Notation."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
