import itertools
import argparse
import numpy as np
from scipy.spatial.distance import hamming


def parse_args():
    """
    This function takes the arguments provided at the command line and parses them to use
    below.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--i5", help="Number of barcodes of type i5", type=int, required=True
    )
    parser.add_argument(
        "--i7", help="Number of barcodes of type i7", type=int, required=True
    )
    parser.add_argument(
        "--i5nn", help="Number of barcodes of type i5nn", type=int, required=True
    )
    parser.add_argument(
        "--i7nn", help="Number of barcodes of type i7nn", type=int, required=True
    )
    parser.add_argument(
        "--outfile",
        "-o",
        help="File to which barcodes will be written. E.g.: 'combinations.csv' ",
        type=str,
        required=True,
    )

    return parser.parse_args()


def generate_combinations(i5: int, i7: int, i5nn: int, i7nn: int) -> list:
    """
    This function generates all the possible combinations of barcodes, given the
    number of each kind.
    i5: int, number of unique i5 barcodes
    i7: int, number of unique i7 barcodes
    i5nn: int, number of unique i5nn barcodes
    i7nn: int, number of unique i7nn barcodes

    returns: list containing lists with possible barcode combinations
    """

    # Each number in list represents a unique barcode of that kind to order
    bc_1 = list(range(1, (i5 + 1)))  # i5
    bc_2 = list(
        range(1, (i7 + 1))
    )  # i7 - prefer the most of these because they are less $$
    bc_3 = list(range(1, (i5nn + 1)))  # i5nn
    bc_4 = list(range(1, (i7nn + 1)))  # i7nn

    # Make a list of barcode lists
    list_lists = [bc_1, bc_2, bc_3, bc_4]

    # Return all possible combinations
    return [p for p in itertools.product(*list_lists)]


def limit_by_hamming_dist(combinations: list):
    """
    This function limits the possible barcode combinations so that there is a minimum Hamming distance among them
    (in this case 2, may make this optional in the future)
    combinations: list of all possible barcode combinations (numeric lists)

    returns: filtered list of barcode combinations
    """

    # Initialize the final list of barcode combinations with the first possible combo
    final = list([combinations[0]])

    # Iterate
    for i in range(len(combinations)):
        if i != 0:
            hdists = []
            for c in final:
                h_dist = hamming(combinations[i], c) * len(final[0])
                hdists = hdists + [h_dist]
            if not any(x < 2 for x in hdists):
                final = final + [combinations[i]]

    return final


def write_combinations(barcode_combinations: list, outfile: str):
    """
    This function takes the barcode combinations list of lists and converts it to readable numpy array
    barcode_combinations: Filtered list of barcodes (as lists)
    outfile: file to write the barcode combinations to

    returns: Barcode combinations written to file, to be used for identifying samples stored in .csv etc.
    Note that there is no header on the outfile.
    """
    np_final = np.array(barcode_combinations)
    np.savetxt(outfile, np_final, delimiter=",")


def main():
    """
    Wrapper to run the whole thing :)
    """

    args = parse_args()

    barcode_list = limit_by_hamming_dist(
        generate_combinations(i5=args.i5, i7=args.i7, i5nn=args.i5nn, i7nn=args.i7nn)
    )

    print(len(barcode_list))

    write_combinations(barcode_combinations=barcode_list, outfile=args.outfile)


if __name__ == "__main__":
    main()
