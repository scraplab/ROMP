from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='ROMP_psypose',
      version='0.0.1',
      description='Modularized version of ROMP for use in the PsyPose package.',
      url='https://github.com/Arthur151/ROMP',
      author='SCRAP Lab',
      author_email='Landry.S.Bulls@dartmouth.edu',
      license='Apache',
      packages=find_packages(),
      include_package_data=True,
      install_requires=requirements,
      zip_safe=False)