from setuptools import setup, find_packages

setup(
    name='pysaprpa',
    version='1.0',
    packages=find_packages(),
    author='Eoin O\'Mahony',
    author_email='eoinomahony028@gmail.com',
    description='A Python package for automating SAP GUI interactions',
    long_description='UPDATE',
    url='https://github.com/eoinomahon/PySAPRPA',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    install_requires=[
        'pandas',
        'pywin32',
    ],
    python_requires='>=3.11.3',
)