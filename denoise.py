from itertools import product
from PIL import Image

import numpy as np
from tqdm import trange

def valid(p, width, height):
    '''
        checks if a pixel is valid
    '''
    return ((0 <= p[0] < width) and (0 <= p[1] < height))



def N(i, j):
    '''
        returns indices of neighbors of pixel at (i, j)
    '''
    delta = [-1, 0, 1]
    return ((i+di, j+dj) for di, dj in product(delta, delta) if (di, dj) != (0, 0))


def cost(x, y, Ny, alpha, beta):
    '''
        returns the cost function
        E = - log P(x, y)
             = alpha*(1 - 1(y = x)) + beta*(sum (for each q in N(y)) 1 - 1(y - q) )

        x : observed pixel, X(i, j)
        y : actual pixel, Y(i, j)
        Ny : neighbors of (i, j) in Y
        alpha : reconstruction 
        beta : smoothness 
    '''
    width, height = X.shape

    term1 = (x != y)
    term2 = sum(n != y for n in Ny)

    return alpha*term1 + beta*term2

def icm(X, alpha, beta):
    width, height = X.shape

    Y = np.array(X)

    for iteration in range(3):
        Ycurrent = np.array(Y)
        for i in trange(width):
            for j in range(height):
                x = X[i, j]
                Ny = [Y[p] for p in N(i, j) if valid(p, width, height)]
                
                cost0 = cost(x, 0, Ny, alpha, beta)
                cost1 = cost(x, 1, Ny, alpha, beta)

                # print (cost0, cost1)
                Ycurrent[i, j] = np.argmin([cost0, cost1])
        Y = Ycurrent
    return Y

X = np.array(Image.open('snoisy.png').convert('1'))
Y = icm(X, 2, 1)
Image.fromarray(Y).save('sdenoised1.png')

# width, height = X.shape
# print (list(product(range(width), range(height))))
# print (sum (cost(X, X, i, j, 0.1, 0.2) for i, j in product(range(width), range(height))))
