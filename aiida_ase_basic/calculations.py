"""
Calculations provided by aiida_ase_basic.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from __future__ import absolute_import

import six

from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData
from aiida.plugins import DataFactory

StructureData = DataFactory('structure')
DiffParameters = DataFactory('ase_basic')


class ASECalculation(CalcJob):
    """
    AiiDA calculation plugin for tracking the provenance of ASE calculations.
    """

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super(ASECalculation, cls).define(spec)
        spec.input('metadata.options.resources', valid_type=dict, default={'num_machines': 1, 'num_mpiprocs_per_machine': 1})
        spec.input('metadata.options.parser_name', valid_type=six.string_types, default='ase_basic')
        spec.input('metadata.options.output_filename', valid_type=six.string_types, default='ase.out')
        #spec.input('parameters', valid_type=DiffParameters, help='Command line parameters for diff')
        spec.input('script', valid_type=SinglefileData, help='ASE script.')
        spec.input('structure', valid_type=StructureData, help='Atomic structure.', required=False)
        spec.input_namespace('files', valid_type=SinglefileData, dynamic=True, required=False, help="Add arbitrary input files needed by the run.")
        spec.output_namespace('files', valid_type=SinglefileData, dynamic=True, help="Output files produced by the run that are stored for further processing.")

        spec.exit_code(100, 'ERROR_MISSING_OUTPUT_FILES', message='Calculation did not produce all expected output files.')


    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files needed by
            the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()
        codeinfo.cmdline_params = [self.inputs.script.filename]
        codeinfo.code_uuid = self.inputs.code.uuid
        #codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        local_copy_list = [ (self.inputs.script.uuid, self.inputs.script.filename, self.inputs.script.filename) ]


        # this is minimalistic - one could add things here like:
        #  * if something is passed to the top-level "structure" input, write the file out in a given format
        #  * if type of file is X, pre-process using procedure Y
        #  * ...
        if 'files' in self.inputs:
            for f in self.inputs.files:
                node = self.inputs.files[f]
                local_copy_list.append( (node.uuid, node.filename, node.filename) )

        calcinfo.local_copy_list = local_copy_list
        calcinfo.retrieve_list = ['*']

        return calcinfo
