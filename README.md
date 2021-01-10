# RAD-barcodes
Tools for RADseq barcodes

Useage for ``barcode_sequences.py``:

```
python barcode_sequences.py --first_barcode <..> --min_dist <..> --restrict_sites <site1 site2>
```
e.g.:
```
python barcode_sequences.py --first_barcode 'AACCCG' --min_dist 3 --restrict_sites CCGG CTGCAG
```
Note that excluding restriction enzyme cut sites with ``--restrict_sites`` is optional, and no filtering will occur if the ``--restrict_sites`` argument is empty, e.g.:
```
python barcode_sequences.py --first_barcode 'AACCCG' --min_dist 3 --restrict_sites
```