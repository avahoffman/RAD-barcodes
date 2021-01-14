import argparse
from csv import reader
from barcode_sequences import write_barcodes, make_reverse_complement


def parse_args():
    """
    This function takes the arguments provided at the command line and parses them to use
    below.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--infile",
        "-i",
        help="File from which barcodes will be read. Should be .csv or .txt with each barcode on a separate line.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-outfile",
        "-o",
        help="File to which barcodes and complement will be written. Should be .csv. E.g.: 'Compliments_out.csv' ",
        type=str,
        required=True,
    )

    return parser.parse_args()


def read_barcodes(infile: str) -> list:
    """
    This function reads barcodes in from file, so that reverse complements can be made.
    infile: file containing barcodes

    returns: list of barcodes in format ['barcode', 'barcode', ..]
    """
    with open(infile, "r") as csv_file:
        csv_reader = reader(csv_file, delimiter=",")
        list_of_rows = list(csv_reader)

    # Initialize with empty list
    flattened = []

    # Iterate through, building the flattened list
    for bc in list_of_rows:
        joined = "".join(bc)
        flattened = flattened + [joined]

    return flattened


def main():
    """
    Wrapper to run the whole thing :)
    """

    args = parse_args()

    barcodes_in = read_barcodes(infile=args.infile)
    reverse_complements = make_reverse_complement(barcodes=barcodes_in)

    write_barcodes(
        barcodes=barcodes_in, outfile=args.outfile, complements=reverse_complements
    )


if __name__ == "__main__":
    main()
