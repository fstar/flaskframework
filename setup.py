"""安装文件"""
import os
from setuptools import setup, find_packages

file_dir = os.path.dirname(__file__)

version_file = os.path.join(file_dir, '.version')

with open(version_file, 'r') as f:
    version = f.readline()

readme_file = os.path.join(file_dir, 'README.md')

with open(readme_file, 'r') as f:
    long_description = f.read()

setup(name='fx-flask',
      packages=find_packages(),
      package_data={'': ['*.yml', '*.ini']},
      version=version,
      entry_points={'console_scripts': ['fx-flask=fx_flask.command_line:cli']},
      include_package_data=True,
      python_requires='>=3.7.0')
