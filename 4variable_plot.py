import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
import pandas as pd

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.set_size_inches(20, 15)

ax.set_ylabel('X-slip (ang)')
ax.set_xlabel('Y-slip (ang)')
ax.set_zlabel('Rotation Angle (deg)')

ax.set_xlim([1,6])
ax.set_ylim([1,6])
ax.set_zlim([1,3])
   
dfe = pd.read_csv("phixyenergy-f_1-6_truncated-500.xyz", header=None)
dfv = pd.read_csv("varphixy-f_1-6_truncated-500.xyz", sep="\t", header=None)
    
dfen = dfe.to_numpy()
dfvn = dfv.to_numpy()

dfen = np.reshape(dfen, (500,))

dfvnx = dfv[0].to_numpy()
dfvny = dfv[1].to_numpy()
dfvnz = dfv[2].to_numpy()

img = ax.scatter(dfvnz, dfvny, dfvnx, c=dfen, cmap=plt.jet(), s=150)

labelsxy = ['0.0', '0.3', '0.6', '0.9', '1.2', '1.5', '1.8', '2.1', '2.4', '2.7', '3.0', '3.3', '3.6', '3.9', '4.2', '4.5', '4.8', '5.1', '5.4', '5.7', '6.0']

labelsz = ['18', '20', '22']


a = np.linspace(0, 21, 21)
b = np.linspace(1, 3, 3)

ax.set_xticks(a)
ax.set_yticks(a)
ax.set_zticks(b)

ax.set_xticklabels(labelsxy, rotation='vertical')
ax.set_yticklabels(labelsxy)
ax.set_zticklabels(labelsz, rotation='vertical')


fig.colorbar(img, ticks=np.linspace(0, 36, 19), format='%.2f', fraction=0.02, pad=0.04, label='Energy (kcal/mol)')

plt.show()
#plt.savefig('phixy1-6-macro_scan_trunc.png')
