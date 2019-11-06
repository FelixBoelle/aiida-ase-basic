"""
Test script that uses ASE to run an EMT calculation

Script partly from the ASE intro tutorials
https://wiki.fysik.dtu.dk/ase/tutorials/surface.html
"""

# --------------------- STEP 1: Prepare the atoms/structure object ------------
#from ase.build import fcc111
#h = 1.85
#d = 1.10

#atoms = fcc111('Cu', size=(4, 4, 2), vacuum=10.0)
#atoms.write('atoms_in.json', format='json')

from ase.io import read
atoms = read('atoms_in.json')

# ==================== START ASE SCRIPT to AiiDA ==============================
from ase.calculators.emt import EMT
from ase.optimize import FIRE

# -------------------- STEP 2: Attach the calculator --------------------------
calc = EMT(properties=['energy', 'stress'])
atoms.set_calculator(calc)

# -------------------- STEP 3: run the dynamics -------------------------------
# write optimizer steps to logfile
dyn = FIRE(atoms, trajectory='Cu111.traj', logfile='FIRE.log')
dyn.run(fmax=0.05)

# -------------------- STEP 4: Extract and save results -----------------------

results = {}
results['potential_energy'] = atoms.get_potential_energy()
results['stress'] = atoms.get_stress()

print('potential energy: ', results['potential_energy'])
print('stress: ', results['stress'])

# ==================== END ASE SCRIPT to AiiDA ================================

# NEED TO STORE
# writes last step of optimization to a .json file that is storable in a db
atoms.write('atoms_out.json', format='json')  # to store 1
# FIRE.log file for reference - to store 2
# results as entry in database - to store 3
# reference to Cu111.traj file for provenance - to store 4
