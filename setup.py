import os
import shutil

from setuptools import setup, find_namespace_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from pathlib import Path


SOURCE_BASH_COMPLETION_FILE_NAME = "bash_completion"
TARGET_BASH_COMPLETION_FILE_NAME = ".bash_completion"
CUPIDONE_COMPLETION_FILE = "cupidone_completion"
COMPLETION_DIR = ".bash_completion.d"
HOME_DIR = Path.home().as_posix()

SOURCE_DIR = "cupidone/completion"
SOURCE_BASH_COMPLETION_FILE = f"{SOURCE_DIR}/{SOURCE_BASH_COMPLETION_FILE_NAME}"
SOURCE_CUPIDONE_COMPLETION_FILE = f"{SOURCE_DIR}/{CUPIDONE_COMPLETION_FILE}"

TARGET_COMPLETION_DIR = f"{HOME_DIR}/{COMPLETION_DIR}"
TARGET_BASH_COMPLETION_FILE = f"{HOME_DIR}/{TARGET_BASH_COMPLETION_FILE_NAME}"
TARGET_CUPIDONE_COMPLETION_FILE = f"{TARGET_COMPLETION_DIR}/{CUPIDONE_COMPLETION_FILE}"


class BasePostCommand():
    def _copy_files(self):
        if os.geteuid() == 0:
            raise RuntimeError("Install should be as a non-privileged user")

        if not os.access(SOURCE_DIR, os.R_OK):
            raise IOError("%s not readable from achive" % SOURCE_DIR)

        if not os.path.exists(TARGET_COMPLETION_DIR):
            os.makedirs(TARGET_COMPLETION_DIR)

        if not os.access(TARGET_COMPLETION_DIR, os.W_OK):
            raise IOError("%s not writeable by user" % TARGET_COMPLETION_DIR)

        if not os.path.exists(TARGET_BASH_COMPLETION_FILE):
            os.makedirs(TARGET_BASH_COMPLETION_FILE)

        shutil.copyfile(src=SOURCE_BASH_COMPLETION_FILE, dst=TARGET_BASH_COMPLETION_FILE)

        shutil.copyfile(src=SOURCE_CUPIDONE_COMPLETION_FILE, dst=TARGET_CUPIDONE_COMPLETION_FILE)


class PostDevelopCommand(BasePostCommand, develop):
    def run(self):
        self._copy_files()
        develop.run(self)


class PostInstallCommand(BasePostCommand, install):
    def run(self):
        self._copy_files()
        install.run(self)


def readme():
    with open("README.md") as f:
        return f.read()


attrs = dict(
    name="cupidone",
    version="0.6.0",
    description="CLI to-do list manager",
    keywords=["cli", "todo", "markdown"],
    long_description=readme(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology"
    ],
    url="https://github.com/vikian050194/cupidone",
    author="Kirill Vinogradov",
    author_email="vikian050194@gmail.com",
    license="MIT",
    license_files=["LICENSE"],
    package_data={
        "cupidone": ["completion/*"]
    },
    packages=find_namespace_packages(where=".", exclude=["tests*"], include=["*"]),
    install_requires=[],
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
    },
    entry_points = {
        "console_scripts": ["cupidone=cupidone.app:run"],
    },
    include_package_data=True,
    zip_safe=True
)

setup(**attrs)
