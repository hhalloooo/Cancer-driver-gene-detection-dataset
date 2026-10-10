"""Join the six data parts and extract the archive."""
from pathlib import Path
import shutil
import zipfile

root = Path(__file__).resolve().parent
archive = root / 'benchmark_data.zip'
with archive.open('wb') as output:
    for number in range(1, 7):
        with (root / f'benchmark_data.zip.part{number:03d}').open('rb') as part:
            shutil.copyfileobj(part, output)
with zipfile.ZipFile(archive) as data:
    data.extractall(root / 'benchmark_data')
print('Data extracted to', root / 'benchmark_data')
