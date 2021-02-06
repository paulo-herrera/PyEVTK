from distutils.core import setup
from evtk.version import PYEVTK_VERSION

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
    package_dir = {'evtk' : 'evtk'},
    package_data = {'evtk' :  ['LICENSE', 'examples/*.py']},
    project_urls={
        "Bug Tracker": "https://github.com/paulo-herrera/PyEVTK",
        "Documentation": "https://github.com/paulo-herrera/PyEVTK",
        "Source Code": "https://github.com/paulo-herrera/PyEVTK",
    }
)
