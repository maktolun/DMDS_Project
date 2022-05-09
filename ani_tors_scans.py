from google.colab import drive
drive.mount('/content/drive')

%cd /content/drive/MyDrive/Colab_Notebooks/project

!pip install torchani
!pip install ase

from ase.optimize import BFGS
from ase import units
from ase.io import read, write
from ase.constraints import FixInternals
import matplotlib.pyplot as plt
import numpy as np
import torchani
import sys

model_names = ['ANI1x', 'ANI1ccx', 'ANI2x']
atoms = read('{}'.format(sys.argv[1]))
mol_name = sys.argv[1].replace('.xyz', '')
stepsize = int(sys.argv[2])
 
ANI1x_energy, ANI1ccx_energy, ANI2x_energy = [], [], []

for torsion in torsion_angles:
    atoms.set_dihedral(8,1,15,20, torsion, mask=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    dihedral_indices = [8,1,15,20]
    dihedral = [atoms.get_dihedral(*dihedral_indices), dihedral_indices]
    c = FixInternals(dihedrals_deg=[dihedral])
    atoms.set_constraint(c)
    print ('\n', 'Dihedral angle set to: ', torsion)
    for model in model_names:
        if model == 'ANI1x':
            calculator = torchani.models.ANI1x().ase()
        elif model == 'ANI1ccx':
            calculator = torchani.models.ANI1ccx().ase()
        elif model == 'ANI2x':
            calculator = torchani.models.ANI2x().ase()
        atoms.set_calculator(calculator)
        opt = BFGS(atoms)
        print ('\n', '{} optimization running ...'.format(model))
        opt.run(fmax=0.0001,steps=1000)
        
        if model == 'ANI1x':
            ANI1x_energy.append(torchani.units.ev2kcalmol(atoms.get_total_energy()))
        elif model == 'ANI1ccx':
            ANI1ccx_energy.append(torchani.units.ev2kcalmol(atoms.get_total_energy()))
        elif model == 'ANI2x':
            ANI2x_energy.append(torchani.units.ev2kcalmol(atoms.get_total_energy()))

        write('{}_{}_{}_opt.xyz'.format(mol_name, torsion, model), atoms, append=True)

ANI1x_energy = [val - min(ANI1x_energy) for val in ANI1x_energy]
ANI1ccx_energy = [val - min(ANI1ccx_energy) for val in ANI1ccx_energy]
ANI2x_energy_diff = [val - min(ANI2x_energy) for val in ANI2x_energy]

out_filename = mol_name + '-opt-aseenergies.dat'
outfile = open(out_filename, "a")
outfile.write('Dihedral' + '\t' + 'E (kcal/mol)' + '\n')

for i in range(len(ANI2x_energy)):
  outfile.write(str(torsion_angles[i]) + '\t' + str(ANI2x_energy[i]) + '\n')

outfile.close()

fig = plt.figure()
plt.plot(torsion_angles, ANI1x_energy, 'b',  marker='.', label='ANI1x')
plt.plot(torsion_angles, ANI1ccx_energy, 'r',  marker='.', label='ANI1ccx')
plt.plot(torsion_angles, ANI2x_energy, 'g',  marker='.', label='ANI2x')
plt.plot(torsion_angles, ANI2x_energy_diff, 'y', marker='.', label='ANI2x_relative')
plt.title('Relative torsional energy scan of ANI-relaxed conformers')
plt.xlabel('Torsion angle (degrees)')
plt.ylabel('Energy (kcal/mol)')
plt.legend(loc = 'upper right')
plt.savefig('torsion-scan.png')
plt.ticklabel_format(useOffset=False)