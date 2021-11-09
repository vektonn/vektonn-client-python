import os

from setuptools import setup, find_packages

package_version = os.environ.get('PYTHON_PACKAGE_VERSION') or '0.dev'

setup(
    name='vektonn',
    version=package_version,
    description='Python client for Vektonn',
    license='Apache License 2.0',
    url='https://github.com/vektonn/vektonn-client-python',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'aiohttp~=3.8',
        'requests~=2.26',
    ],
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
