from setuptools import setup, find_packages

setup(
    name='PyJail',
    version='0.1.2',
    author='Mrigank Pawagi',
    author_email='mrigankpawagi@gmail.com',
    description='A Python module for sandboxing code execution.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mrigankpawagi/PyJail',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    install_requires=[
        dep.strip() for dep in open('requirements.txt').readlines()
    ],
)
