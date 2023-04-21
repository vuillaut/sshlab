from setuptools import setup, find_packages
import os

# Read the version from sshlab/version.py
version = {}
with open(os.path.join("sshlab", "version.py")) as f:
    exec(f.read(), version)

setup(
    name='sshlab',
    version=version['__version__'],
    description='A tool for launching Jupyter Notebooks on remote servers using SSH',
    long_description=open('README.md',  encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Thomas Vuillaume',
    author_email='thomas.vuillaume@lapp.in2p3.fr',
    url='https://github.com/vuillaut/sshlab',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
    ],
    extras_require={
        'doc': [
            'sphinx',
            'furo',
        ]
    },
    entry_points={
        'console_scripts': [
            'sshlab=sshlab.sshlab:main',
            'sshlab-kill=sshlab.sshlab_kill:main',
            'sshlab-tensorboard=sshlab.sshtensorboard:main'
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
