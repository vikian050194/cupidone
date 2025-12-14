import os
import shutil

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from pathlib import Path


BASH_COMPLETION_FILE = ".bash_completion"
CUPIDONE_COMPLETION_FILE = "cupidone_completion"
COMPLETION_DIR = ".bash_completion.d"
HOME_DIR = Path.home().as_posix()

TARGET_COMPLETION_DIR = f"{HOME_DIR}/{COMPLETION_DIR}"
TARGET_BASH_COMPLETION_FILE = f"{HOME_DIR}/{BASH_COMPLETION_FILE}"
TARGET_CUPIDONE_COMPLETION_FILE = f"{TARGET_COMPLETION_DIR}/{CUPIDONE_COMPLETION_FILE}"

SOURCE_DIR = "cupidone/completion"
SOURCE_BASH_COMPLETION_FILE = f"{SOURCE_DIR}/{BASH_COMPLETION_FILE}"
SOURCE_CUPIDONE_COMPLETION_FILE = f"{SOURCE_DIR}/{CUPIDONE_COMPLETION_FILE}"


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        self._copy_files()
        install.run(self)

    def _copy_files(self):
        if os.geteuid() == 0:
            raise RuntimeError("Install should be as a non-privileged user")

        if not os.access(SOURCE_DIR, os.R_OK):
            raise IOError("%s not readable from achive" % SOURCE_DIR)

        if not os.access(TARGET_COMPLETION_DIR, os.W_OK):
            raise IOError("%s not writeable by user" % TARGET_COMPLETION_DIR)

        # if not os.path.exists(TARGET_BASH_COMPLETION_FILE):
        shutil.copyfile(src=SOURCE_BASH_COMPLETION_FILE, dst=TARGET_BASH_COMPLETION_FILE)

        if not os.path.exists(TARGET_COMPLETION_DIR):
            os.makedirs(TARGET_COMPLETION_DIR)

        # if not os.path.exists(TARGET_CUPIDONE_COMPLETION_FILE):
        shutil.copyfile(src=SOURCE_CUPIDONE_COMPLETION_FILE, dst=TARGET_CUPIDONE_COMPLETION_FILE)


def readme():
    with open("README.md") as f:
        return f.read()


attrs = dict(
    name="cupidone",
    version="0.2.0",
    description="CLI todo list manager",
    long_description=readme(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities"
    ],
    url="https://github.com/vikian050194/cupidone",
    author="Kirill Vinogradov",
    author_email="vikian050194@gmail.com",
    license="MIT",
    packages=find_packages(where=".", exclude=["tests*"], include="*"),
    install_requires=[],
    test_suite="nose.collector",
    tests_require=["nose"],
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
    },
    entry_points = {
        "console_scripts": ["cupidone=cupidone.app:run"],
    },
    include_package_data=True,
    zip_safe=False
)

setup(**attrs)
