# ***********************************************************************************
# * Copyright 2010-2019 Paulo A. Herrera. All rights reserved.                           *
# *                                                                                 *
# * Redistribution and use in source and binary forms, with or without              *
# * modification, are permitted provided that the following conditions are met:     *
# *                                                                                 *
# *  1. Redistributions of source code must retain the above copyright notice,      *
# *  this list of conditions and the following disclaimer.                          *
# *                                                                                 *
# *  2. Redistributions in binary form must reproduce the above copyright notice,   *
# *  this list of conditions and the following disclaimer in the documentation      *
# *  and/or other materials provided with the distribution.                         *
# *                                                                                 *
# * THIS SOFTWARE IS PROVIDED BY PAULO A. HERRERA ``AS IS'' AND ANY EXPRESS OR      *
# * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF    *
# * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO      *
# * EVENT SHALL <COPYRIGHT HOLDER> OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,        *
# * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,  *
# * BUT NOT LIMITED TO, PROCUREMEN OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,    *
# * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY           *
# * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING  *
# * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS              *
# * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                    *
# ***********************************************************************************

# CHECK THIS PATCH
#try:
#    from setuptools import setup
#except ImportError:
from distutils.core import setup

from src.version import PYEVTK_VERSION

def readme(fname):
    with open(fname, 'r') as f:
        return f.read()

setup(
    name = 'evtk',
    version = PYEVTK_VERSION,
    description = 'Exports data as binary VTK files',
    long_description = readme('README.md'),
    author = 'Paulo Herrera',
    author_email = 'paulo.herrera.eirl@gmail.com',
    url = 'https://github.com/paulo-herrera/PyEVTK.git',
    packages = ['evtk'],
    package_dir = {'evtk' : 'src'},
    package_data = {'evtk' :  ['LICENSE', 'examples/*.py']},
    project_urls={
        "Bug Tracker": "https://github.com/paulo-herrera/PyEVTK",
        "Documentation": "https://github.com/paulo-herrera/PyEVTK",
        "Source Code": "https://github.com/paulo-herrera/PyEVTK",
    }
)

