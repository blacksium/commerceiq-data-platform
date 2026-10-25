# Data Sources

## Dataset attribution

Dataset: Brazilian E-Commerce Public Dataset by Olist
Provider: Olist and dataset collaborators
Platform: Kaggle
URL: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
Downloaded: 2026-10-25

License listed by the publisher: CC BY-NC-SA 4.0
License reference: https://creativecommons.org/licenses/by-nc-sa/4.0/

Thanks to Olist and its collaborators for making the dataset available.

The dataset license is separate from any license applied to this
project's original code.

## Source snapshot

Downloaded archive: archive.zip
CSV files extracted: 9

Archive SHA-256:

967e41e04fc306fe604e2a693f488995a8b41e5047418f8a5c8e4abd6deca784

The Kaggle dataset version number was not recorded at download.
The archive and CSV checksums identify the local snapshot used.

CSV checksums are recorded in docs/source_checksums.sha256.

## Local storage

Extracted source files: data/raw/olist/

The original archive and extracted CSV files are kept outside Git.
Original source files are not edited during discovery.

Historical source data and any future synthetic data must remain
distinguishable.

## Reproduce the source setup

1. Download the dataset ZIP from the source URL.
2. Test the archive:

   python3 -m zipfile -t ~/Downloads/archive.zip

3. Create the extraction folder:

   mkdir -p data/raw/olist

4. Extract the archive:

   python3 -m zipfile -e ~/Downloads/archive.zip data/raw/olist

5. From the repository root, verify the CSV files:

   sha256sum -c docs/source_checksums.sha256

If a checksum differs, investigate the source version or file changes.
Do not overwrite the recorded checksums simply to make verification pass.

A differently packaged ZIP can have a different archive checksum
while containing identical CSV files. Check the CSV fingerprints too.

## Scope of checksum verification

Matching checksums establish that file contents match the recorded
snapshot. They do not establish business accuracy or source authenticity.