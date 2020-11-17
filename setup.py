from setuptools import setup,find_packages
setup(
        name='plotHicGenome',
        author="chenjhbio",
        author_email="chenjunhui@genomics.cn",
        description="THis package was used for showing Hicproc or juicerbox matrix",
        keywords="Hicproc, juicer",
        url="http://example.com/HelloWorld/",
        project_urls={
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
        classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Python Software Foundation License'
    ],
        py_modules=['plotHicmain'],
	packages=find_packages(),
        include_package_data=True,
        version='0.1.1',
        install_requires=[
        'matplotlib',
        'numpy',
        'scipy',
	'pandas'
    ],
    entry_points = {
    'console_scripts': [
        'plotHicGenome=plotHicmain:main'
    ]
}
)
