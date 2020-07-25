from PIL import Image
import numpy as np 
from tqdm import trange

Ileft = np.array(Image.open('im3.png').convert('L'), dtype=np.int32)
Iright = np.array(Image.open('im4.png').convert('L'), dtype=np.int32)

height, width = Ileft.shape
print (height, width)


def D(qi, i):
    ''' Unary cost
    qi : disparity at position i
    i : position of pixel
    '''
    if i + qi >= width: return np.nan

    return abs(left[i] - right[i-qi])

def V(qi, qj):
    ''' Pairwise cost
    qi : disparity at position i 
    qj : disparity at position i+1  
    '''
    return (qi - qj)**2

Q = 16 # disparities 0,  1, 2, .. , 15

all_disparities = []
for line in trange(height):
    left = Ileft[line]
    right = Iright[line]
    disparities = np.ones_like(left)


    # print (sum(D(disparities[i], i) + V(disparities[i], disparities[i+1]) for i in range(width-1)))
    # print (disparities)

    #exit()


    new_forward_messages = np.zeros((width, Q))
    forward_messages = np.zeros((width, Q))

    backward_messages = np.zeros((width, Q))
    new_backward_messages = np.zeros((width, Q))

    # message i is to i to i-1
    # i = 0, m = 0
    # i = 1, m[0->1]

    for i in range(0, width-1):
        for qi in range(Q):
            new_forward_messages[i+1][qi] = np.nanmin([D(q, i) + V(q, qi) + forward_messages[i][q] for q in range(Q)])


    # message i is to i to i+1

    # i = 1, m[1<-0]

    for i in range(1, width):
        for qi in range(Q):
            new_backward_messages[i-1][qi] = np.nanmin([D(q, i) + V(q, qi) + backward_messages[i][q] for q in range(Q)])

    forward_messages = np.array(new_forward_messages)
    backward_messages = np.array(new_backward_messages)

    # print (forward_messages)
    # print (backward_messages)

    for i in range(width):
        disparities[i] = np.nanargmin([forward_messages[i][q] + backward_messages[i][q] + D(q, i) for q in range(Q)])

    # print (disparities)
    # print (sum(D(disparities[i], i) + V(disparities[i], disparities[i+1]) for i in range(width-1)))
    all_disparities.append(np.array(disparities))
