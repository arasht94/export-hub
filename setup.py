from setuptools import setup, find_packages

setup(
    name='export-hub',
    version='0.1.0',
    description='Repository of Torch Export Graphs',
    author='Arash Taheri',
    author_email='',
    url='https://github.com/yourusername/export-hub',
    packages=find_packages(),
    install_requires=[
        'Flask==3.0.0',
        'jinja2==3.1.2',
    ],
    python_requires='>=3.8',
)

