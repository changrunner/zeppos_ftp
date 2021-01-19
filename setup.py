from setuptools import setup, find_packages
from decouple import Config, RepositoryEnv


def parse_requirements_from_pipfile():
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open('Pipfile'))
    requirements_pipfile_style = [line for line in lineiter]
    start_index = requirements_pipfile_style.index('[packages]') + 1
    end_index = requirements_pipfile_style.index('[requires]') - 1
    requirements = list(map(lambda x: x.replace(' = "', '').replace('"', ''),
                            requirements_pipfile_style[start_index:end_index]))
    return requirements


env_package_config = Config(RepositoryEnv('.env_package'))
env_project_config = Config(RepositoryEnv('.env_project'))

#Getting the content of the README.md so it become the text display on pypi.org
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=env_project_config('project_name'),
    version=env_package_config('package_version'),
    author=env_project_config('author'),
    author_email=env_project_config('author_email'),
    description=env_project_config('description'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=parse_requirements_from_pipfile(),
    license='Apache License 2.0',
    url=env_project_config('url'),
    # Classifiers can be found at: https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
