"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

from codecs import open # to maintain consistent encoding. May or may not use. TODO: remove if unused
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'VERSION.txt'), encoding='utf-8') as f:
    version = f.read()

setup(name='vertica_parity',
      version=version,
      description='A set of scripts to setup a local vertica test environment',
      # The project's main homepage.
      url='https://www.github.com',
      author='Joshua Icuss',
      author_email='jicuss@gmail.com',
       # Choose your license
      license='',
      classifiers=[
        'Programming Language :: Python :: 2.7',
      ],
      packages=find_packages(exclude=['notes_do_not_include','logs','cache','vertica_parity_environment']),

      # Include non-python files found in each package in the install.
      include_package_data=True,

      package_data={
        # If any package contains *.json files, include them:
        '': ['*.json', '*.sql', ],
      },
      install_requires=['pyodbc'],
      tests_require=['mock'],
      test_suite='tests',

      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[dev,tests]
      extras_require={
        'dev': [
            'mock',
        ],
        'rel': [
            'mock',
            'wheel'
        ]
      },

      entry_points={
        'console_scripts': [
            'parse_workflow=entry_points:parseWorkflow',
            'create_copy_commands=entry_points:createCopyCommands',
            'generate_example_copy_json=entry_points:generateExampleCopyJSON',
        ],
      },

)