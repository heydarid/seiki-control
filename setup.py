from setuptools import setup

setup(
    name='seikicontrol',
    version='0.1.0',    
    description='Python package that controls the DS102 series motor controller.',
    url='https://github.com/heydarid/seiki-control',
    author='D. Heydari, M. Catuneanu',
    author_email='dheydari@stanford.edu',
    license='BSD 2-clause',
    packages=['seikicontrol'],
    install_requires=['mpi4py>=2.0',
                      'numpy',
                      'pyserial==3.4'                     
                      ],
)