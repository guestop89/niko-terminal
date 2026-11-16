#!/usr/bin/env python3
"""Installation locale de Niko Terminal, sans dépendance Python externe."""
from pathlib import Path
import re
import shutil
import datetime

source = Path(__file__).resolve().parent
home = Path.home()
bin_dir = home / '.local/bin'
app_dir = home / '.config/niko-terminal'
config = home / '.config/fish/config.fish'
for folder in (bin_dir, app_dir, config.parent):
    folder.mkdir(parents=True, exist_ok=True)
old = config.read_text() if config.exists() else ''
if config.exists():
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    shutil.copy2(config, config.with_name(f'config.fish.before-niko-{stamp}'))
shutil.copy2(source / 'niko.py', bin_dir / 'niko-banner')
(bin_dir / 'niko-banner').chmod(0o755)
shutil.copy2(source / 'niko.fish', app_dir / 'niko.fish')
block = '''# >>> Niko Terminal >>>
source "$HOME/.config/niko-terminal/niko.fish"
# <<< Niko Terminal <<<'''
pattern = r'# >>> Niko Terminal >>>.*?# <<< Niko Terminal <<<'
if re.search(pattern, old, re.S):
    updated = re.sub(pattern, lambda _: block, old, flags=re.S)
else:
    updated = old.rstrip() + '\n\n' + block + '\n'
config.write_text(updated)
print('Niko installé ! Ouvre un nouveau terminal Fish pour le voir.')
print('Une sauvegarde de la configuration précédente a été conservée à côté de config.fish.')
