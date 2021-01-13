# RAD-barcodes

### Barcode organizing tools for sequencing, including:

- A generator for quad-indexed RADseq, to ensure no samples have more than two barcodes in common
- A generator for unique barcodes, given a "starter" barcode
  - Accounts for minimum Hamming distance
  - Removes restriction cut sites of choice

### Barcode combinations using `barcode_combinations.py`

This tool aims to remove problematic effects of [index hopping](https://www.illumina.com/techniques/sequencing/ngs-library-prep/multiplexing/index-hopping.html) on Illumina sequencers. In brief, sample barcodes can "hop" to a different sample, meaning some reads are misidentified. When large numbers of samples are barcoded and pooled, risk of index hopping increases. To avoid this (and avoid having to throw out valuable sequencing data!), Illumina recommends at least two unique barcodes per sample. This is much easier if you are using a 4 barcode approach ("inner" *and* "outer" barcodes), such as described by [Franchini et al. 2017](https://doi.org/10.1111/mec.14077). 

Here is an example. Let's say you have 2 unique barcodes each of your inner (i5 and i7) and outer (i5nn and i7nn) barcodes. If you only care that combinations are unique, you'd get ![2^4](https://render.githubusercontent.com/render/math?math=2%5E4) = 16 barcodes.. but this could lead to index hopping if you had more samples in a sequencing lane. This script filters barcode combinations that have a Hamming distance of less than 2. So in the previous example, combination 1112 (1st of i5, i7, i5nn, and second i7nn) would be excluded as too similar to 1111 (1st of all barcodes). Hamming distance for that example is only =1. Hamming distance between 1111 and 1122 =2 though, so it's good!

#### Usage

```
python barcode_combinations.py --i5 <int> --i7 <int> --i5nn <int> --i7nn <int>
```
e.g.:
```
$ python barcode_combinations.py --i5 5 --i7 5 --i5nn 6 --i7nn 6
```
The generator will write an array of combinations that you can assign to samples. The number of samples that can be processed with the given barcode scheme will also print to console.

### Barcode generator using `barcode_sequences.py`

#### Useage

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
