from setuptools import setup, find_packages
from pathlib import Path

setup(
	name='portmap',
	version='0.1.0',
	author='Joseph',
	author_email='josephdove@proton.me',
	description='A TCP self-hostable reverse proxy server',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
	classifiers=[
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
    packages=find_packages(
        include=[
            "portmap",
            "portmap.*"
        ]
    ),
	entry_points={
		"console_scripts": [
			"portmap = portmap.portmapc:main",
		]
	},
	python_requires='>=3.6',
)