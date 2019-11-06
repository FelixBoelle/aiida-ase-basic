# -*- coding: utf-8 -*-
"""Submit a test calculation on localhost.

Usage: verdi run submit.py
"""
from __future__ import absolute_import
from __future__ import print_function
import os
import click
from aiida.plugins import CalculationFactory
from aiida.orm import StructureData, SinglefileData
from aiida.engine import run

def example_emt(ase_code):
    import ase

    # see script.py for wrapped ASE instructions
    script = SinglefileData(file=os.path.abspath('./script.py'))
    structure = StructureData

    # structure
    from ase.build import fcc111
    h = 1.85
    d = 1.10
    atoms = fcc111('Cu', size=(4, 4, 2), vacuum=10.0)
    #structure = StructureData(ase=atoms)
    atoms.write('atoms_in.json', format='json')
    structure = SinglefileData(file=os.path.abspath('./atoms_in.json'))

    # set up calculation
    inputs = {
        'code': ase_code,
        'script': script,
        'files': {
            'structure': structure,
        },
        'metadata': {
            'description': "Test ASE EMT calculator",
        },
    }

    # Note: in order to submit your calculation to the aiida daemon, do:
    # from aiida.engine import submit
    # future = submit(CalculationFactory('ase_basic'), **inputs)
    result = run(CalculationFactory('ase_basic'), **inputs)

    #import pdb; pdb.set_trace()
    new_coords = result['files']['atoms_out'].get_content()
    print("Relaxed coordinates: \n{}".format(new_coords))

@click.command('cli')
@click.argument('codelabel')
def cli(codelabel):
    """Click interface"""
    from aiida.common.exceptions import NotExistent
    from aiida.orm import Code
    import sys
    try:
        code = Code.get_from_string(codelabel)
    except NotExistent:
        print("The code '{}' does not exist".format(codelabel))
        sys.exit(1)
    example_emt(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
