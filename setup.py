"""
Setup configuration
"""
from setuptools import setup, find_packages

setup(
    name='poker-engine',
    version='1.0.0',
    author='Max Alpatov',
    author_email='rider16@yandex.ru',
    description='An advanced poker game library.',
    packages=find_packages(),
    # install_requires=[
    #     'numpy>=1.19.0',
    #     'typing_extensions>=3.7.4',
    # ],
    license='MIT License',
    keywords='poker game engine casino',
    url='https://github.com/yourusername/poker-engine',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
