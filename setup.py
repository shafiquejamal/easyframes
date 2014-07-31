from distutils.core import setup

setup(
    name='EasyFrames',
    version='0.1.7',
    author='Shafique Jamal',
    author_email='shafique.jamal@gmail.com',
    packages=['easyframes', 'easyframes.test'],
    scripts=['bin/sample_script.py'],
    url='http://pypi.python.org/pypi/EasyFrames/',
    license='LICENSE.txt',
    description='Classes and methods for executing stata-like commands easily for pandas dataframes.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pandas >= 0.14.1",
        "numpy >= 1.8.1",
    ],
)