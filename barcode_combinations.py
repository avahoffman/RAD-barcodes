import itertools
import numpy as np
from scipy.spatial.distance import hamming


def generate_combinations():
	
	# Each number in list represents a unique barcode of that kind to order
	bc_1 = list(range(1,13)) # i5
	bc_2 = list(range(1,31)) # i7 - prefer the most of these because they are less $$
	bc_3 = list(range(1,14)) # i5nn
	bc_4 = list(range(1,14)) # i7nn
	
	# Make a list of barcode lists
	list_lists = [bc_1, bc_2, bc_3, bc_4]
	
	# Return all possible combinations
	return [p for p in itertools.product(*list_lists)]
	

def limit_by_hamming_dist(list: combinations):

comb = generate_combinations()

final = list([comb[0]])
for i in range(len(comb)):
	if i != 0:
		hdists = []
		for combination in final:
			h_dist = hamming(comb[i], combination) * len(final[0])
			hdists = hdists + [h_dist]
		if not any(x < 2 for x in hdists):
			final = final + [comb[i]]


print(len(final))

np_final = np.array(final)
np.savetxt('barcode_combinations.csv', np_final, delimiter=',')