import time
import numpy as np
import torch
import numpy.linalg as la
from scipy.stats import norm
import sys
## Adding PyGRANSO directories. Should be modified by user
sys.path.append(r'C:\Users\Buyun\Documents\GitHub\PyGRANSO')
from pygranso import pygranso
from pygransoStruct import Options, Data

# Please read the documentation on https://pygranso.readthedocs.io/en/latest/
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# variables and corresponding dimensions.
d1 = 5
d2 = 10
var_in = {"M": (d1,d2),"S": (d1,d2)}

# data_in
data_in = Data()
torch.manual_seed(1)
data_in.eta = .5
data_in.Y = torch.randn(d1,d2).to(device=device, dtype=torch.double)

# user defined options
opts = Options()
opts.x0 = .2 * torch.ones((2*d1*d2,1)).to(device=device, dtype=torch.double)
# opts.print_ascii = True

#  main algorithm  
start = time.time()
soln = pygranso(var_in,data_in,opts)
end = time.time()
print("Total Wall Time: {}s".format(end - start))

# print(soln.final.x)