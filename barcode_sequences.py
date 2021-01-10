import sys
import itertools
import argparse
from typing import Tuple
from scipy.spatial.distance import hamming


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--first_barcode', '-c', help='number of barcodes', type=str, required=True)
	parser.add_argument('--min_dist', '-s', help='minimum hamming distance among barcodes', type=int, required=True)
	parser.add_argument('--restrict_sites', '-r', help='restriction cutsites to exclude from barcodes', type=str, nargs="*", required=False)
	
	return parser.parse_args()


def generate_combinations(n:int) -> list:
	"""
	This function generates all the possible combinations of N number of base positions
	*Assumes that all bases can be A, C, G, or T
	n: number of digits in barcode	
	"""
	
	# Each number locus can be A, C, G, or T
	bases = ["A", "C", "G", "T"]
	
	# Make a list of barcode lists
	list_lists = [bases]*n
	
	# Return all possible combinations
	return [p for p in itertools.product(*list_lists)]
	

def filter_by_hamming(first_bc:str, combinations:Tuple, min_dist:int)->list:
	# Initialize the first barcode.
	final = list([tuple(first_bc)])
	
	# Iterate
	for i in range(len(combinations)):
		if i != 0:
			hdists = []
			for c in final:
				h_dist = hamming(combinations[i], c) * len(final[0])
				hdists = hdists + [h_dist]
			if not any(x < min_dist for x in hdists):
				final = final + [combinations[i]]
	
	return final


def flatten_barcodes(barcodes:list):
	# Flatten list to make barcodes easier to read
	flattened = []
	
	for bc in barcodes:
		joined = ''.join(bc)
		flattened = flattened + [joined]
	
	return flattened
		

def filter_restriction_sites(barcodes:list, restriction_cutsites:list):
	# Remove restriction sites
	res_removed = []
	
	# Check that the barcode does not contain any of the specified cut sites!
	for bc in barcodes:
		if not any(x in bc for x in restriction_cutsites):
			res_removed = res_removed + [bc]
	
	return res_removed
	
	
def write_barcodes(barcodes:list, outfile:str):
	# Write barcodes
	with open(outfile, mode="w") as outfile:
		for bc in barcodes:
			outfile.write("%s\n" % bc)
			

def main():
	"""
	Wrapper to run the whole thing
	"""
	
	args = parse_args()
	
	# Generate list of possible barcodes given the length of what's provided
	combinations = generate_combinations(n = len(args.first_barcode))
	
	# Generate hamming distance limited list of barcodes
	hamming_bcs = filter_by_hamming(first_bc = args.first_barcode, combinations = combinations, min_dist = args.min_dist)
	
	flat_bcs = flatten_barcodes(barcodes = hamming_bcs)
	
	res_removed_bcs = filter_restriction_sites(barcodes = flat_bcs, restriction_cutsites = args.restrict_sites)

	print(len(res_removed_bcs),"barcodes retained, with",len(flat_bcs)-len(res_removed_bcs),"excluded\
	due to restriction cut sites.")
	
	
if __name__ == "__main__":
	main()
	