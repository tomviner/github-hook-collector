from setuptools import setup

setup(
    name='github-hook-collector',
    version='0.1.0-dev',
    package_dir={'': 'github_hook_collector'},
    packages=['github_hook_collector'],
    install_requires=['django>=1.7.1'],
)

