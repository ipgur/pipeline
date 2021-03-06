"""
Package setup.

=======
License
=======
Copyright (c) 2017 Thomas Lehmann

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
from setuptools import setup, find_packages
from spline.version import VERSION


def get_long_description():
    """Reading long description from a file."""
    file_path = os.path.join(os.path.dirname(__file__), 'spline.rst')
    with open(file_path) as handle:
        return handle.read()


setup(name='spline',
      version=VERSION,
      description='(s)hell oriented (p)ipe(line) tool for ci/cd',
      long_description=get_long_description(),
      author='Thomas Lehmann',
      author_email='thomas.lehmann.private@gmail.com',
      license="MIT",
      install_requires=["click", "pyaml", "jinja2", "schema"],
      packages=find_packages(exclude=['tests', 'tests.*']),
      scripts=['scripts/spline', 'scripts/spline-loc'],
      package_data={'spline': [
          'components/templates/docker-container.sh.j2',
          'components/templates/docker-image.sh.j2',
          'components/templates/packer-image.sh.j2',
          'components/templates/ansible.sh.j2',
          'components/templates/python-script.sh.j2',
          'tools/report/templates/report.html.j2',
          'tools/loc/templates/spline-loc.yml.j2']},
      keywords="pipeline tool ci/cd bash docker packer ansible python",
      url="https://github.com/Nachtfeuer/pipeline",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Unix",
          "Environment :: Console",
          "Topic :: Utilities"
      ])
