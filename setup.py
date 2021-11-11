import os

from setuptools import setup, find_packages

package_version = os.environ.get('VEKTONN_PYTHON_PACKAGE_VERSION') or '0.0.0.dev0'

setup(
    name='vektonn',
    version=package_version,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7',
    install_requires=[
        'aiohttp~=3.8.0',
        'orjson~=3.6.4',
        'pydantic~=1.8.2',
        'requests~=2.26.0',
    ],
)
