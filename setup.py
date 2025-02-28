from setuptools import setup, find_packages

setup(
    name="codetrace",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.34.0",
        "datasets>=2.14.0",
        "nnsight",
        "numpy",
        "pandas",
        "tqdm",
        "torchtyping",
        "typeguard>=2.11.1,<3.0.0",
        "accelerate",
        "tree-sitter",
        "tree-sitter-python",
    ],
) 