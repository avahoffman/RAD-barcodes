# RAD-barcodes

### Barcode organizing tools for sequencing, including:

- A generator for quad-indexed RADseq, to ensure no samples have more than two barcodes in common
- A generator for unique barcodes, given a "starter" barcode
  - Accounts for minimum Hamming distance
  - Removes restriction cut sites of choice

### Barcode combinations using `barcode_combinations.py`

This tool aims to remove problematic effects of [index hopping](https://www.illumina.com/techniques/sequencing/ngs-library-prep/multiplexing/index-hopping.html) on Illumina sequencers. In brief, sample barcodes can "hop" to a different sample, meaning some reads are misidentified. When large numbers of samples are barcoded and pooled, risk of index hopping increases. To avoid having to throw out valuable sequencing data, Illumina recommends at least two unique barcodes per sample. This is much more affordable if you are using a 4-barcode approach ("inner" *and* "outer" barcodes), such as described by [Franchini et al. 2017](https://doi.org/10.1111/mec.14077). 

Here's an example. Let's say you have 2 unique i5 barcodes (A, B), i7 barcodes (C, D), i5nn barcodes (E, F), and i7nn barcodes (G, H). If you only care that combinations are unique, you'd get ![2^4](https://render.githubusercontent.com/render/math?math=2%5E4) = 16 barcodes. **However** this means some samples share all but one barcode, leading to greater risk of index hopping. A better approach would be one that ensures at least two barcodes differ.

This script filters barcode combinations that have a Hamming distance of less than 2 when compared to the first barcode (with strikethrough):

|   | AC  | AD  | BC  | BD  |
|---|---|---|---|---|
| **EG**  | ACEG  | <s>ADEG  | <s>BCEG  | BDEG  |
| **EH**  | <s>ACEH  | ADEH  | BCEH  | <s>BDEH  |
| **FG**  | <s>ACFG  | ADFG  | BCFG  | <s>BDFG  |
| **FH**  | ACFH  | <s>ADFH  | <s>BCFH  | BDFH  |

#### Usage

```
python barcode_combinations.py --i5 <int> --i7 <int> --i5nn <int> --i7nn <int> --outfile <filename>
```
e.g.:
```
$ python barcode_combinations.py --i5 5 --i7 5 --i5nn 6 --i7nn 6 --outfile 'combinations.csv'
```
The generator will write an array of combinations that you can assign to samples. The number of samples that can be processed with the given barcode scheme will also print to console.

### Barcode generator using `barcode_sequences.py`

This tool aims to generate unqiue barcodes given a "seed" barcode to begin building. The generator assumes normal bases (A, C, G, T) and barcodes of the same length. Any other filtering (such as GC content) can be done by the user on the output file.

There are a few inputs to consider:
  - Minimum Hamming distance (how dissimilar should your barcodes be?) 
  - Restriction sites (you want to steer clear of barcodes that can be digested!)



#### Usage

```
python barcode_sequences.py --first_barcode <barcode sequence> --min_dist <minimum Hamming dist> --outfile <filename.csv> --restrict_sites <site1 site2>
```
e.g.:
```
python barcode_sequences.py --first_barcode 'AACCCG' --min_dist 3 --outfile 'bc_out.csv' --restrict_sites CCGG CTGCAG
```
Note that excluding restriction enzyme cut sites with ``--restrict_sites`` is optional, and no filtering will occur if the ``--restrict_sites`` argument is empty, e.g.:
```
python barcode_sequences.py --first_barcode 'AACCCG' --min_dist 3 --outfile 'bc_out.csv' --restrict_sites
```
