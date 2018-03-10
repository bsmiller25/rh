from setuptools import setup

setup(name='rh',
      version='0.1',
      description='Messing around with Robinhood.io',
      url='https://github.com/bsmiller25/rh',
      author='Ben Miller',
      author_email='bsmiller25@gmail.com',
      packages=['rh'],
      install_requires=[
          'numpy',
          'Robinhood',
          ],
      dependency_links=['https://github.com/Jamonek/Robinhood/tarball/master#egg=Robinhood-1.0.1'],
      zip_safe=False)
