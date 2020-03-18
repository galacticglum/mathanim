import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='mathanim',
    version='1.0.0',
    author='Shon Verch',
    description='A tool for creating stylized maths presentations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/galacticglum/mathanim',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)