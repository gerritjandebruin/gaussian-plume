"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.rst').read_text(encoding='utf-8')

setup(
    name='GaussianPlume',  
    version='0.1.0',   
    description='Calculation of Gaussian plumes', 

    # long_description=long_description,  # Optional
    # long_description_content_type='text/markdown',  # Optional (see note above)
    # url='https://github.com/pypa/sampleproject',  # Optional

    author='TNO EMSA', 

    author_email='robbert.bloem@tno.nl', 

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Scientists',

        # Pick your license as you wish
        # 'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='science',  # Optional

    package_dir={'': 'src'},  
    packages=find_packages(where='src'),  
    python_requires='>=3.8, <4',

    # install_requires=[''],  # Optional, see requirements.txt
    # extras_require={  # Optional
        # 'dev': ['check-manifest'],
        # 'test': ['coverage'],
    # },

    # package_data={  # Optional
        # 'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # entry_points={  # Optional
        # 'console_scripts': [
            # 'sample=sample:main',
        # ],
    # },

    # project_urls={  # Optional
        # 'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        # 'Source': 'https://github.com/pypa/sampleproject/',
    # },
)