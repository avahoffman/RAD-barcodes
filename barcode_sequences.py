import itertools
import sys
from typing import Tuple
import numpy as np
from scipy.spatial.distance import hamming


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
	
	
def filter_barcodes(first_bc:Tuple, combinations:list, min_dist:int, restriction_cutsites:Tuple=()):
	"""
	"""
	
	# Confirm initialized barcode is appropriate for combinations provided
	if not len(first_bc) == len(combinations[0]):
		sys.exit("Error! Number of bases in first barcode must match number of bases in \
		provided combinations")
	
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
	
	print(len(final))
	
	# Flatten list to make barcodes easier to read
	with open('barcodes_for_use.csv', mode="w") as outfile:
		for bc in final:
			joined = ''.join(bc)
			
			# Check that the barcode does not contain any of the specified cut sites!
			if not any(x in joined for x in restriction_cutsites):
				# Write each barcode as a new line
				outfile.write("%s\n" % joined)
		

c = generate_combinations(n=6)

filter_barcodes(first_bc='AACCCG', combinations=c, min_dist=3, restriction_cutsites=('CCGG','CTGCAG'))
