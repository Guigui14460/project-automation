# Autonation of project creation for developers.

## Table of contents
1. [Usage of the application](#usage)

## Usage

For Windows :

```shell
$ pyinstaller cli.py --exclude-module=autopep8 --hidden-import=pkg_resources.py2_warn --name automate_projects --onefile
```

For Unix-like systems :

```shell
$ pyinstaller cli.py --exclude-module=autopep8 --hidden-import=pkg_resources.py2_warn --name automate_projects --onefile
```
