from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='InsightLog',
    version='1.2.3',
    packages=find_packages(), 
    license='MIT',
    description='A customizable logging utility with enhanced features for developers.',
    author='VelisCore',
    author_email='velis.help@web.de',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/VelisCore/InsightLogger',
    download_url='https://github.com/VelisCore/InsightLog/archive/refs/tags/v1.2.3.tar.gz',
    keywords=[
        'logging', 'log', 'logger', 'developer tools', 'performance monitoring', 'visualization'
    ],
    install_requires=[
        'termcolor',
        'matplotlib',
        'tabulate',
        'psutil',
        'tqdm',
    ],
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/VelisCore/InsightLog/issues',
        'Documentation': 'https://github.com/VelisCore/InsightLog/wiki',
        'Source Code': 'https://github.com/VelisCore/InsightLog',
    },
)
