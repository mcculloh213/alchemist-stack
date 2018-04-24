from distutils.core import setup

setup(
    # Application Name:
    name='alchemist_stack',

    # Version Number:
    version='0.1.0',

    # Application Author Details:
    author='H.D. "Chip" McCullough IV',
    author_email='hdmccullough.work@gmail.com',

    # Packages:
    packages=['alchemist_stack'],

    # Include Additional Files into the Package:
    include_package_date=True,

    # Details:
    url='https://github.com/mcculloh213/alchemist-stack',
    license='LICENSE.md',
    description='A Thread-Safe, Multi-Session/Multi-Connection Model-Repository-Context base for SQL Alchemy',
    long_description=open('README.md').read(),

    # Dependent Packages (Distributions):
    install_requires=[
        'sqlalchemy',
    ],
)