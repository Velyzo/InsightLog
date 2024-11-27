from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='InsightLog',
    version='1.1',
    packages=find_packages(), 
    license='MIT',
    description='A better logging utility with enhanced features.',
    author='Eldritchy',
    author_email='eldritchy.help@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Eldritchy/InsightLog',
    download_url='https://github.com/Eldritchy/InsightLog/archive/refs/tags/v1.1.tar.gz',
    keywords=[
        'eldritchy', 'logging', 'log', 'logger', 'better', 'utility', 'developer tools'
    ],
    install_requires=[
        'termcolor',
        'tqdm',
    ],
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/Eldritchy/InsightLog/issues',
        'Documentation': 'https://github.com/Eldritchy/InsightLog/wiki',
        'Source Code': 'https://github.com/Eldritchy/InsightLog',
    },
)