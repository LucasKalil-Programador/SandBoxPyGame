from setuptools import setup, find_packages

setup(
    name='sand-box-python',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/LucasKalil-Programador/sand-box-python',
    license='MIT License',
    author='Lucas G. Kalil',
    author_email='lucas.prokalil2020@outlook.com',
    description='Simple sandbox game where each pixel on the screen represents an element',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pygame',
        'numba',
        'numpy',
    ],
)
