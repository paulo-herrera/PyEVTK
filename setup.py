######################################################################################
# MIT License
# 
# Copyright (c) 2010-2021 Paulo A. Herrera
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
######################################################################################

from setuptools import setup

exec(open("evtk/version.py").read())

setup(
    name = 'evtk',
    version = __version__,
    description = 'Exports data as binary VTK files',
    long_description = open("README.md").read(),
    author = 'Paulo Herrera',
    author_email = 'paulo.herrera.eirl@gmail.com',
    url = 'https://github.com/paulo-herrera/PyEVTK.git',
    license = "MIT",
    packages = ['evtk'],
    package_dir = {'evtk' : 'evtk'},
    package_data = {'evtk' :  ['LICENSE', 'examples/*.py']},
    project_urls={
        "Bug Tracker": "https://github.com/paulo-herrera/PyEVTK",
        "Documentation": "https://github.com/paulo-herrera/PyEVTK",
        "Source Code": "https://github.com/paulo-herrera/PyEVTK",
    }
)
