from setuptools import setup

setup(
    name='github-hook-collector',
    version='0.1.0-dev',
    package_dir={'': 'src'},
    packages=['github_hook_collector', 'collector'],
    # Can't find a way to specify a dev version
    # of Django here.
    install_requires=[
        'psycopg2',
        'django_extensions',
    ],
    tests_require=[
        'tox',
        'pytest',
        'requests',
    ],
)
