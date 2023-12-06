import numpy as np

a = np.array(([[1, 2, 3, 4, 5], 
                [6, 7, 8, 9, 10], 
                [11, 12, 13, 14, 15], 
                [16, 17, 18, 19, 20], 
                [21, 22, 23, 24, 25],
                [1,1,1,1,1]]))

diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]

# Now back to the original array to get the upper-left-to-lower-right diagonals,
# starting from the right, so the range needed for shape (x,y) was y-1 to -x+1 descending.
diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))

# Another list comp to convert back to Python lists from numpy arrays,
# so it prints what you requested.
print([n.tolist() for n in diags])
