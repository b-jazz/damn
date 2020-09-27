#!/usr/bin/env python
import setuptools


setup_args = {
    'name': 'damn',
    'version': '0.0.1',
    'description': 'Periodically check the discharge rate of the given dam and alert if above some value.',
    'author': 'Bryce Jasmer',
    'author_email': 'b-jazz@users.noreply.github.com',
    'install_requires': [
        'Click',
        'geopy',
        'requests',
        'simplejson',
        ],
}


_SRC_DIR = 'src'
setup_args['package_dir'] = {'': _SRC_DIR}
setup_args['packages'] = setuptools.find_packages(_SRC_DIR)
setup_args['entry_points'] = {
    'console_scripts': ['damn = damn.damn:main'],
}


setuptools.setup(**setup_args)
# End of file.
