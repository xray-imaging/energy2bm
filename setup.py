from setuptools import setup, find_packages

setup(
    name='ops',
    version=open('VERSION').read().strip(),
    #version=__version__,
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/xray-imaging/2bm-ops',
    packages=find_packages(),
    include_package_data = True,
    scripts=['bin/energy'],
    description='ops',
    zip_safe=False,
)

