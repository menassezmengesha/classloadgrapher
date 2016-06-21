#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
from graphviz import Digraph

from classloadgrapher import __version__
from classloadgrapher import template

import argparse
import sys
import logging


class ClassloadGrapher:
    __author__ = "mzm"
    __copyright__ = "mzm"
    __license__ = "new-bsd"

    _logger = logging.getLogger(__name__)

    _legend = template.__template__

    def openFile(self, fname):
        try:
            _f = open(fname)
        except IOError as e:
            print("I/O error({0}) : {1}".format(e.errno, e.strerror))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception("Very unexpected error")
        return _f

    def graphClassload(self, dot, fname, regex, abrv=True):
        sigs = set()

        _file = self.openFile(fname)

        for line in _file:
            items = line.split(" ")

            if ((items[0] == "RESOLVE")):
                from_class = items[1]
                to_class = items[2]

                abrv_from = ""
                abrv_to = ""

                if (regex is not None):
                    if (regex in from_class or regex in to_class):
                        continue

                from_class = from_class.rstrip()
                to_class = to_class.rstrip()
                sig = hash(from_class + to_class)
                toSig = hash(to_class)
                if (sig not in sigs and toSig not in sigs and '[' not in to_class):
                    sigs.add(sig)
                    sigs.add(toSig)
                    if (abrv):
                        abrv_from_list = from_class.split(".")
                        for abrv_from_package in abrv_from_list:
                            abrv_from += abrv_from_package[:1] + '.'
                        abrv_to_list = to_class.split(".")
                        for abrv_to_package in abrv_to_list:
                            abrv_to += abrv_to_package[:1] + '.'
                        dot.edge(abrv_from + from_class.split(".")[-1], abrv_to + to_class.split(".")[-1])
                    else:
                        dot.edge(from_class, to_class)
        _file.close()

    def addLegend(self, dot, template=_legend):
        subdot = Digraph('legend', node_attr={'shape': 'plaintext'})
        subdot.node('_legend', template)
        dot.subgraph(subdot)

    def parse_args(self, args):
        """
        Parse command line parameters

        :param args: command line parameters as list of strings
        :return: command line parameters as :obj:`argparse.Namespace`
        """
        parser = argparse.ArgumentParser(
            description="A tool to make a graph of loaded classes in a jvm")
        parser.add_argument(
            '--version',
            action='version',
            version='Classload-Grapher {ver}'.format(ver=__version__))
        parser.add_argument(
            dest="raw",
            help="class load trace file",
            type=str,
            metavar="trace_file")
        parser.add_argument(
            dest="dest",
            help="destination for generated file",
            type=str,
            metavar="destination_file")
        parser.add_argument(
            '-a',
            dest="abrv",
            help="Abbreviate e.g. java.lang. -> j.l.",
            type=bool)
        parser.add_argument(
            '-f',
            dest="filter",
            help="Filter",
            type=str)
        parser.add_argument(
            '-v',
            '--verbose',
            dest="loglevel",
            help="set loglevel to INFO",
            action='store_const',
            const=logging.INFO)
        parser.add_argument(
            '-vv',
            '--very-verbose',
            dest="loglevel",
            help="set loglevel to DEBUG",
            action='store_const',
            const=logging.DEBUG)
        return parser.parse_args(args)

    def main(self, args):
        args = self.parse_args(args)
        logging.basicConfig(level=args.loglevel, stream=sys.stdout)
        self._logger.debug("Start graphing...")
        dot = Digraph(node_attr={'shape': 'plaintext'}, comment='Loaded Classes')
        self.graphClassload(dot, args.raw, args.filter, args.abrv)
        self.addLegend(dot)
        dot.render(args.dest, view=True)
        self._logger.info("Ends here")

    def run(self):
        self.main(sys.argv[1:])

    def __init__(self):
        self.run()


def run():
    ClassloadGrapher()


if __name__ == "__main__":
    ClassloadGrapher()
