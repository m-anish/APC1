from setuptools import setup, find_packages

setup(
    name='APC1',
    version='0.1.0',
    description='MicroPython library to interface with APC1 weather sensor',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Anish Mangal',
    author_email='anishmg@umich.edu',
    license='GPLv3',
    packages=find_packages(where='apc1'),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,  # To include non-Python files like README.md
)
