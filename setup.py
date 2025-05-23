from setuptools import setup, find_packages

setup(
    name='pjenergy',  # nome do pacote (evite acentos ou espaços)
    version='0.1.0',
    description='Projeto de análise energética',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        # dependências que você pode precisar, ex:
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
