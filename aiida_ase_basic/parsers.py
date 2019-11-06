# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_ase_basic.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from __future__ import absolute_import

import os
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory

ASECalculation = CalculationFactory('ase_basic')


class DiffParser(Parser):
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
        from aiida.common import exceptions
        super(DiffParser, self).__init__(node)
        if not issubclass(node.process_class, ASECalculation):
            raise exceptions.ParsingError("Can only parse ASECalculation")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        from aiida.orm import SinglefileData

        output_filename = self.node.get_option('output_filename')

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
                    output_node = SinglefileData(file=handle)

                self.out('files.{}'.format(os.path.splitext(filename)[0]), output_node)

        return ExitCode(0)
