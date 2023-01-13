from setuptools import setup, find_packages

setup(
    name='energy2bm',
    version=open('VERSION').read().strip(),
    #version=__version__,
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/xray-imaging/energy2bm',
    packages=find_packages(),
    include_package_data = True,
    scripts=['bin/energy'],
    description='ops',
    zip_safe=False,
)

