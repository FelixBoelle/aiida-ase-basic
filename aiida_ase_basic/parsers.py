# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_ase_basic.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from __future__ import absolute_import

import os
import json
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
from aiida import orm
from aiida.common import exceptions

ASECalculation = CalculationFactory('ase_basic')


class AseParser(Parser):
    """
    Parser class for parsing output of calculation.
    """
    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a ASECalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        super(AseParser, self).__init__(node)
        if not issubclass(node.process_class, ASECalculation):
            raise exceptions.ParsingError("Can only parse ASECalculation")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        from aiida.orm import SinglefileData

        # first check if folder was retrieved at all
        try:
            output_folder = self.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER

        # output_filename = self.node.get_option('output_filename')

        # # Check that folder content is as expected
        # files_retrieved = self.retrieved.list_object_names()
        # files_expected = [output_filename]
        # # Note: set(A) <= set(B) checks whether A is a subset of B
        # if not set(files_expected) <= set(files_retrieved):
        #     self.logger.error("Found files '{}', expected to find '{}'".format(
        #         files_retrieved, files_expected))
        #     return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # figure out which files were input
        input_files = []
        for label in self.node.inputs:
            node = self.node.inputs[label]
            if isinstance(node, SinglefileData):
                input_files.append(node.filename)

        for filename in self.retrieved.list_object_names():
            # select some output files for further parsing
            # logic based on file extension could go here
            if filename not in input_files and filename.endswith('json'):
                self.logger.info("Adding '{}'".format(filename))
                with self.retrieved.open(filename, 'rb') as handle:
                    #output_node = SinglefileData(file=handle)
                    output_node = orm.Dict(dict=json.load(handle))

                self.out('files.{}'.format(os.path.splitext(filename)[0]),
                         output_node)

        # before exiting with exitcode 0 check the stderr file for errors
        # look at warnings
        std_err_file = '_scheduler-stderr.txt'
        with output_folder.open(std_err_file, 'r') as handle:
            errors = handle.read()
            for line in errors.split('\n'):
                if 'Error' in line:
                    self.logger.error(f'Found error in {std_err_file}: {line}')
                    return self.exit_codes.ERROR_STDERR_SCHEDULER

        return ExitCode(0)
