from setuptools import find_packages, setup

from shorty.version import __VERSION__

dependencies=[
    'django',
    'django-autoconfig',
    'django-nuit',
]
test_dependencies=[
    'django-setuptest',
]

setup(
    name='djshorty',
    version=__VERSION__,
    description='A Django URL shortening app',
    author='Ben Cardy',
    author_email='ben.cardy@ocado.com',
    packages=find_packages(),
    install_requires=dependencies,
    # To run tests via python setup.py test
    tests_require=test_dependencies,
    test_suite='setuptest.setuptest.SetupTestSuite',
    include_package_data=True,
)
