"""Extract a validated Benue location snapshot; never infer voter counts."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from locations import LGAS


def extract(path):
    names = {name.casefold(): name for name in LGAS}
    records, codes, wards = [], set(), set()
    with path.open(encoding='utf-8-sig', newline='') as source:
        reader = csv.DictReader(source)
        required = {'state', 'lg', 'ward', 'code', 'location', 'state_code', 'lg_code', 'ward_code', 'pu_code'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('CSV is missing required location columns.')
        for line, row in enumerate(reader, 2):
            if (row.get('state') or '').strip().casefold() != 'benue':
                continue
            if None in row or any(not (row.get(key) or '').strip() for key in required):
                raise ValueError(f'Incomplete Benue row at line {line}.')
            lga = names.get(row['lg'].strip().casefold())
            if not lga:
                continue
            code = row['code'].strip()
            expected = '/'.join(row[key].strip() for key in ('state_code', 'lg_code', 'ward_code', 'pu_code'))
            if not lga or not code.startswith('07/') or code != expected:
                raise ValueError(f'Invalid Benue hierarchy at line {line}.')
            if code in codes:
                raise ValueError(f'Duplicate Benue PU code at line {line}: {code}')
            codes.add(code)
            record = dict(lga=lga, ward=row['ward'].strip().upper(), code=code, name=row['location'].strip().upper())
            records.append(record)
            wards.add((lga, record['ward']))
    if {row['lga'] for row in records} != set(LGAS):
        raise ValueError('The source does not cover all nine Benue South LGAs.')
    records.sort(key=lambda row: row['code'])
    metadata = dict(source_file=path.name, source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                    description='User-supplied Nigeria polling-unit CSV; publication date and current official completeness unknown.',
                    polling_units=len(records), wards=len(wards), lgas=len(LGAS),
                    by_lga=dict(sorted(Counter(row['lga'] for row in records).items())),
                    voter_totals='Not provided. Unknown totals remain NULL; no estimates or zeros are inferred.')
    return records, metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    records, metadata = extract(args.source)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'benue_directory.json').write_text(json.dumps(records, indent=2) + '\n')
    (args.output / 'benue_directory_source.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, indent=2))
