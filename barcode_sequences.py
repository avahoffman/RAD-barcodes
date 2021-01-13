import itertools
import argparse
from scipy.spatial.distance import hamming


def parse_args():
    """
    This function takes the arguments provided at the command line and parses them to use
    below.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--first_barcode", "-c", help="number of barcodes", type=str, required=True
    )
    parser.add_argument(
        "--min_dist",
        "-s",
        help="minimum hamming distance among barcodes",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--restrict_sites",
        "-r",
        help="restriction cutsites to exclude from barcodes",
        type=str,
        nargs="*",
        required=False,
    )

    return parser.parse_args()


def generate_combinations(n: int) -> list:
    """
    This function generates all the possible combinations of N number of base positions
    *Assumes that all bases can be A, C, G, or T
    n: number of digits in barcode

    returns: list of lists containing possible barcode combinations for n digits
    """

    # Each number locus can be A, C, G, or T
    bases = ["A", "C", "G", "T"]

    # Make a list of barcode lists
    list_lists = [bases] * n

    # Return all possible combinations
    return [p for p in itertools.product(*list_lists)]


def filter_by_hamming(first_bc: str, combinations: list, min_dist: int) -> list:
    """
    This function filters a list of possible barcodes to give a minimum hamming distance.
    Hamming distance is important to ensure no two barcodes are too similar. This
    function will iteratively build a list, ensuring that no barcode added is too similar
    to a barcode already contained within the growing list.

    first_bc: The first barcode you'll be using - it's used to seed comparisons.
    combinations: Possible barcodes to choose from (those too similar based on Hamming distance are excluded)
    min_dist: Minimum allowable hamming distance

    returns: filtered list of barcodes (which are themselves lists)
    """
    # Initialize the first barcode
    final = list([tuple(first_bc)])

    # Iterate
    for i in range(len(combinations)):
        if i != 0:
            hdists = []

            # Check against each barcode already present in the list for hamming dist.
            for c in final:
                h_dist = hamming(combinations[i], c) * len(final[0])
                hdists = hdists + [h_dist]

            # If the barcode is not too close to any already in the list, it is then
            # included.
            if not any(x < min_dist for x in hdists):
                final = final + [combinations[i]]

    # Return barcodes that satisfy the specified Hamming distance
    return final


def flatten_barcodes(barcodes: list):
    """
    This function 'flattens' the list of barcodes, making them easier to read, e.g.:
    ['A','A','C','G'] -> ['AACG']

    returns: list of flattened barcodes
    """
    # Initialize with empty list
    flattened = []

    # Iterate through, building the flattened list
    for bc in barcodes:
        joined = "".join(bc)
        flattened = flattened + [joined]

    return flattened


def filter_restriction_sites(barcodes: list, restriction_cutsites: list):
    """
    This function filters out any barcodes that contain a restriction enzyme cut site -
    check the enzymes being used in your reactions!! Cut sites should be given 5'->3'.

    e.g., MspI is CCGG.

    If none are provided (empty list) none are removed.

    barcodes: list of barcodes to be filtered (must have already been flattened)
    restriction_cutsites: list of cut sites

    returns: filtered list of barcodes
    """
    # Initialize with empty list
    res_removed = []

    # Check that the barcode does not contain any of the specified cut sites!
    for bc in barcodes:
        if not any(x in bc for x in restriction_cutsites):
            res_removed = res_removed + [bc]

    return res_removed


def write_barcodes(barcodes: list, outfile: str):
    # Write barcodes
    with open(outfile, mode="w") as outfile:
        for bc in barcodes:
            outfile.write("%s\n" % bc)


def main():
    """
    Wrapper to run the whole thing :)
    """

    args = parse_args()

    # Generate list of possible barcodes given the length of what's provided
    combinations = generate_combinations(n=len(args.first_barcode))

    # Generate hamming distance limited list of barcodes
    hamming_bcs = filter_by_hamming(
        first_bc=args.first_barcode, combinations=combinations, min_dist=args.min_dist
    )

    flat_bcs = flatten_barcodes(barcodes=hamming_bcs)

    res_removed_bcs = filter_restriction_sites(
        barcodes=flat_bcs, restriction_cutsites=args.restrict_sites
    )

    print(
        len(res_removed_bcs),
        "barcodes retained, with",
        len(flat_bcs) - len(res_removed_bcs),
        "excluded due to restriction cut sites.",
    )


if __name__ == "__main__":
    main()
