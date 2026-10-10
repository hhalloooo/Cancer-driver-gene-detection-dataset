"""Verify, reassemble and extract the benchmark data with the Python standard library."""
from pathlib import Path
import hashlib
import json
import zipfile

def main():
    root=Path(__file__).resolve().parent
    meta=json.loads((root/'download_manifest.json').read_text())
    archive=root/'benchmark_data.zip'
    # Verify every part before writing the assembled archive.
    for part in meta['parts']:
        path=root/part['name']
        if not path.is_file(): raise FileNotFoundError('Missing download: '+part['name'])
        content=path.read_bytes()
        if len(content)!=part['bytes'] or hashlib.sha256(content).hexdigest()!=part['sha256']:
            raise ValueError('Corrupted download: '+part['name'])
    with archive.open('wb') as handle:
        for part in meta['parts']: handle.write((root/part['name']).read_bytes())
    assert archive.stat().st_size==meta['archive_bytes']
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==meta['archive_sha256']
    target=root/'benchmark_data'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for member in z.infolist():
            dest=(target/member.filename).resolve()
            if not dest.is_relative_to(target.resolve()): raise ValueError('Unsafe archive path')
        z.extractall(target)
    print('Verified and extracted data to',target)

if __name__=='__main__': main()
