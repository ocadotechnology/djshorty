from setuptools import find_packages, setup

from shorty.version import __VERSION__

dependencies=[
    'django',
    'django-autoconfig >= 0.5.0',
    'django-nuit >= 1.0.0, < 2.0.0',
]
test_dependencies=[
    'django-setuptest',
    'mock',
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
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
)
