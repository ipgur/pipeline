"""Represent the main entry point for the spline loc tool."""
# Copyright (c) 2018 Thomas Lehmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# pylint: disable=no-self-use, cell-var-from-loop
import sys
import os
import platform
import logging
import multiprocessing
import re

import click
from yaml import safe_load

from spline.tools.logger import Logger
from spline.tools.adapter import Adapter
from spline.tools.query import Select
from spline.tools.table import pprint


class Application(object):
    """Spline loc application."""

    def __init__(self, **options):
        """
        Initialize application with command line options.

        Args:
            options (ApplicationOptions): given command line options.
        """
        self.options = options
        self.logging_level = logging.DEBUG
        self.setup_logging()
        self.logger = Logger.get_logger(__name__)
        self.results = []

    def setup_logging(self):
        """Setup of application logging."""
        logging_format = "%(asctime)-15s - %(name)s - %(message)s"
        Logger.configure_default(logging_format, self.logging_level)

    def load_configuration(self):
        """Loading configuration."""
        filename = os.path.join(os.path.dirname(__file__), 'templates/spline-loc.yml.j2')
        with open(filename) as handle:
            return Adapter(safe_load(handle)).configuration

    @staticmethod
    def walk_files_for(path, supported_extensions):
        """
        Iterating files for given extensions.

        Args:
            supported_extensions (list): supported file extentsion for which to check loc and com.

        Returns:
            str: yield each full path and filename found.
        """
        for root, _, files in os.walk(path):
            for filename in files:
                extension = os.path.splitext(filename)[1]
                if extension in supported_extensions:
                    yield os.path.join(root, filename), extension

    def analyse(self, path_and_filename, pattern):
        """
        Find out lines of code and lines of comments.

        Args:
            path_and_filename (str): path and filename to parse  for loc and com.

        Returns:
            int, int: loc and com for given file.
        """
        with open(path_and_filename) as handle:
            content = handle.read()
            loc = content.count('\n') + 1
            com = 0
            for match in re.findall(pattern, content, re.DOTALL):
                com += match.count('\n') + 1

            return loc, com

    def run(self):
        """Processing the pipeline."""
        self.logger.info("Running with Python %s", sys.version.replace("\n", ""))
        self.logger.info("Running on platform %s", platform.platform())
        self.logger.info("Current cpu count is %d", multiprocessing.cpu_count())

        configuration = self.load_configuration()
        path = os.path.abspath(Adapter(self.options).path)
        supported_extension = [Adapter(entry).extension for entry in configuration]

        for path_and_filename, extension in Application.walk_files_for(path, supported_extension):
            regex = Select(*configuration) \
                .where(lambda entry: Adapter(entry).extension == extension) \
                .transform(lambda entry: Adapter(entry).regex) \
                .build()[0]

            loc, com = self.analyse(path_and_filename, regex)
            self.results.append({
                'file': path_and_filename.replace(path + '/', ''),
                'loc': loc,
                'com': com,
                'ratio': "%.1f" % (float(com) / float(loc))
            })

        pprint(self.results, keys=['ratio', 'loc', 'com', 'file'])


def main(**options):
    """Spline loc tool."""
    application = Application(**options)
    application.run()
    return application


@click.command()
@click.option('--path', type=str, default=os.getcwd(), help="Path where to parse files")
def click_main(**options):
    """Spline loc tool."""
    main(**options)


if __name__ == "__main__":
    click_main()
