#Mounting Google Drive folders to access files
from google.colab import drive
drive.mount('/content/drive')

#Go to working directory
%cd /content/drive/MyDrive/Colab_Notebooks/project

#Installing TorchANI and ASE
!pip install torchani
!pip install ase

#Importing all required packages
from ase.optimize import BFGS
from ase import units
from ase.io import read, write
from ase.constraints import FixInternals
import matplotlib.pyplot as plt
import numpy as np
import torchani
import sys

#Defining ANI model names, reading user inputs (molecule name and step size for torsional scans)
model_names = ['ANI1x', 'ANI1ccx', 'ANI2x']
atoms = read('{}'.format(sys.argv[1]))
mol_name = sys.argv[1].replace('.xyz', '')
stepsize = int(sys.argv[2])

#Creating lists to store calculated ANI energies
ANI1x_energy, ANI1ccx_energy, ANI2x_energy = [], [], []

##Performing torsional scans with defined torsional angles
for torsion in torsion_angles:
    ##Defining atom indices that form dihedral angle to be fixed
    atoms.set_dihedral(8,1,15,20, torsion, mask=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    dihedral_indices = [8,1,15,20]
    dihedral = [atoms.get_dihedral(*dihedral_indices), dihedral_indices]
    c = FixInternals(dihedrals_deg=[dihedral])
    atoms.set_constraint(c)
    print ('\n', 'Dihedral angle set to: ', torsion)
    ##Setting up calculators and assigning them to the molecule 
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
        ##Running 1000 steps of optimization with maximum force on atoms as 0.0001
        opt.run(fmax=0.0001,steps=1000)
        
        ##Gathering total calculated energies of molecules from each ANI model
        if model == 'ANI1x':
            ANI1x_energy.append(torchani.units.ev2kcalmol(atoms.get_total_energy()))
        elif model == 'ANI1ccx':
            ANI1ccx_energy.append(torchani.units.ev2kcalmol(atoms.get_total_energy()))
        elif model == 'ANI2x':
            ANI2x_energy.append(torchani.units.ev2kcalmol(atoms.get_total_energy()))
        ##Creating XYZ files for optimized structures 
        write('{}_{}_{}_opt.xyz'.format(mol_name, torsion, model), atoms, append=True)

#Calculating relative energies of molecules with respect to the minimum energy
ANI1x_energy = [val - min(ANI1x_energy) for val in ANI1x_energy]
ANI1ccx_energy = [val - min(ANI1ccx_energy) for val in ANI1ccx_energy]
ANI2x_energy_diff = [val - min(ANI2x_energy) for val in ANI2x_energy]

#Creating an output file  with optimized energies
out_filename = mol_name + '-opt-aseenergies.dat'
outfile = open(out_filename, "a")
outfile.write('Dihedral' + '\t' + 'E (kcal/mol)' + '\n')

#Creating an output file  with relative energies
for i in range(len(ANI2x_energy)):
  outfile.write(str(torsion_angles[i]) + '\t' + str(ANI2x_energy[i]) + '\n')

outfile.close()

##Creating energy plots for each model
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
