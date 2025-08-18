from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='InsightLog',
    version='1.5',
    packages=find_packages(), 
    license='MIT',
    description='An advanced, feature-rich logging utility with real-time monitoring, performance profiling, anomaly detection, and comprehensive analytics for Python applications.',
    author='Velyzo',
    author_email='help@velyzo.de',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Velyzo/InsightLogger',
    download_url='https://github.com/Velyzo//InsightLog/archive/refs/tags/v1.5.tar.gz',
    keywords=[
        'logging', 'log', 'logger', 'monitoring', 'performance', 'profiling', 
        'analytics', 'dashboard', 'visualization', 'anomaly detection',
        'system monitoring', 'developer tools', 'debugging', 'metrics',
        'real-time monitoring', 'database logging', 'security logging'
    ],
    install_requires=[
        'termcolor>=2.0.0',
        'matplotlib>=3.5.0',
        'tabulate>=0.9.0',
        'psutil>=5.8.0',
        'numpy>=1.21.0',
        'tqdm>=4.64.0',
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
        'Bug Tracker': 'https://github.com/Velyzo/InsightLog/issues',
        'Documentation': 'https://github.com/Velyzo/InsightLog/wiki',
        'Source Code': 'https://github.com/Velyzo/InsightLog',
    },
)
