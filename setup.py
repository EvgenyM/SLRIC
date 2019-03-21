from setuptools import setup, find_packages
import SLRIC

setup(
    name='SLRIC',
    version=SLRIC.__version__,
    packages=find_packages(),
    url='https://github.com/SergSHV/SLRIC',
    license='MIT',
    author='Fuad Aleskerov, Natalia Meshcheryahkova, Sergey Shvydun(*)',
    author_email='shvydun@hse.ru',
    description='SRIC and LRIC indices calculation',
    long_description=open('README.rst').read(),
    install_requires=[
                       'numpy', 'cvxopt', 'networkx']
)
