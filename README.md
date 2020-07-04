# Autonation of project creation for developers.

This project allows developers to create all kinds of projects (to be included in the executable of course) in a single command line via this CLI.

## Table of contents

1. [How to use the CLI ?](#how-to-use-the-cli)
2. [Simple use](#simple-use)
3. [Executable creation](#compilation)
4. [Env file](#env-file)
5. [General usage](#general-usage)
6. [Licenses options](#licenses-options)
7. [Examples](#examples)
8. [Contribute](#contribute)

## How to use the CLI ?

You need to download this Github repo via this command `git clone https://github.com/Guigui14460/project_automation.git` or `git clone git@github.com:Guigui14460/project_automation.git`.

After that, you need to use `pipenv` command to create the Python virtual environment. You can also use `virtualenv` command.

If you use `pipenv`, just launch:

```shell
$ pipenv install
```

If you use `virtualenv`, launch:

```shell
$ python -m venv env # replace python by python3 on Unix-like systems
$ . env/bin/activate # For Unix-like systems
$ env\Scripts\activate.bat # For Windows system
$ pip install -r requirements.txt
```

**Now, you are ready to begin with !**

## Simple use

Just launch:

```shell
$ python cli.py -h
```

You will have the same results at [general usage section](#general-usage).

**Warning !** If you want to create a project in Python and there are packages to install, the packages will install in the virtual environment of that project and not the desired project.
To avoid this, we advise you to [compile the application](#compilation).

**Warning !** If you want to create a repository on Github, you need to put your login credentials in a `.env` file ([see this section for more informations](#env-file)).

## Compilation

For Windows and Unix-like systems :

```shell
$ pyinstaller cli.py --exclude-module=autopep8 --hidden-import=pkg_resources.py2_warn --name automate_projects --onefile
```

## Env file

For personal use, we advise you to put your identifiers in the `.env` file at the root of the project.
Here is an example of how to write this :

```env
GITHUB_USER=<username>
GITHUB_PASS=<userpass>
GITHUB_OAUTH_ACCESS_TOKEN=<very_long_access_token>
```

You must not use simple or double quotation marks
**Warning !** If you have enabled dual authentication, you are required to use an access token. Here is the [official Github documentation](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). After, you can only specify the `GITHUB_OAUTH_ACCESS_TOKEN`.

If you want to produce your own version to distribute this CLI, or you use a compiled version, you need to place the `.env` file at the same place from your executable file.

## General usage

After [compiling](#compilation), you can use your executable. You can launch it via the `help` command :

```shell
$ automate_projects -h
```

You will have this result :

```
usage: automate_projects [-h] [-i] [--github] [--public] [--license LICENSE]
                         {c,cpp,deno,flutter,go,haskell,java,nodejs,php,python,website}
                         ...

positional arguments:
  {c,cpp,deno,flutter,go,haskell,java,nodejs,php,python,website}
                        Use one of the available sub-command

optional arguments:
  -h, --help            show this help message and exit
  -i, --allow-install   allows to install used commands/packages (False by
                        default)

Github options:
  --github              use the github versioning
  --public              make the github repo with "Public Status"
  --license LICENSE     license type to add for the repo
```

To use subcommands, you can test the `python` subcommand :

```shell
$ automate_projects python -h
```

You will have this result :

```
usage: automate_projects.exe python [-h] [-t {classic,cython}] [--no-env]
                                    [--env {pipenv,venv}]
                                    [-p PACKAGES [PACKAGES ...]]
                                    path project_name

sub-command to generate Python type project

positional arguments:
  path                  path of the parent root for create the project
                        structure
  project_name          name of the project

optional arguments:
  -h, --help            show this help message and exit
  -t {classic,cython}, --type {classic,cython}
                        create some specific python project (classic by
                        default)
  --no-env              no use the python virtual environment (False by
                        default)
  --env {pipenv,venv}   choice a python virtual environment (pipenv by
                        default)
  -p PACKAGES [PACKAGES ...], --packages PACKAGES [PACKAGES ...]
                        package to install for this specific project
```

Each sub-command has its uniqueness, it's up to you to see what you do.

For more information, see [this section](#examples) showing some examples of use ;)

## Licenses options

By default, if you not use Github, the CLI will not add any `LICENSE` file. If you use Github and you not specify any license type, the CLI will add the `unlicense`.

Here is a list of licenses you can use:

```
apache : Apache License 2.0
bsd3 :  BSD 3-Clause "New" or "Revised" License
bsd2 :  BSD 2-Clause "Simplified" License
CC :  Creative Commons Zero v1.0 Universal
eclipse :  Eclipse Public License 2.0
gnu3 :  GNU General Public License v3.0
gnu2 :  GNU General Public License v2.0
gnuAffero3 :  GNU Affero General Public License v3.0
gnuLess3 :  GNU Lesser General Public License v3.0
gnuLess2.1 :  GNU Lesser General Public License v2.1
mit :  MIT License
mozilla :  Mozilla Public License 2.0
unlicense :  Unlicense
```

## Examples

Here are a few examples representing the majority of use cases.

---

### C++ example without Github

```shell
$ automate_projects -i cpp <your_path> <your_project_name>
```

Creation of a simple C++ project. Allow automatic installation of the required programs and packages.

---

### Cython example with Github (public repo)

```shell
$ automate_projects --github --public --license gnu3 -i python <your_path> <your_project_name> -t cython --env pipenv -p numpy matplotlib scipy sympy
```

Here, you choose to create a Python project and install automatically the required programs and packages. We create a public repository on Github licensed under GNU General Public License v3.0. We use use the Pipenv virtual environment. The Python project type is a [Cython](https://cython.readthedocs.io/en/latest/) project and we install [numpy](https://numpy.org/), [matplotlib](https://matplotlib.org/), [scipy](https://www.scipy.org/) and [sympy](https://www.sympy.org/en/index.html) python packages.

---

### Maven example with Github (private repo)

```shell
$ automate_projects --github java <your_path> <your_project_name> <project_package_name> -t mvn -c <compagny_name>
```

Here, you choose to create a Java project and not install the required programs and packages. We create a private repository on Github licensed under Unlicense. The Java project type is a [Maven](https://maven.apache.org/index.html) project.

---

### Webpack example without Github

```shell
$ automate_projects -i nodejs <your_path> <your_project_name> -t webpack
```

Here, you choose to create a [NodeJS project](https://nodejs.org/en/) and install automatically the required programs and packages. The NodeJS project type is a [WebpackJS](https://webpack.js.org/) project. For WebpackJS, some inputs are required to help the CLI to generate all the files and install all the packages.

## Contribute

You can contribute to the project in different ways:

---

### Add commands :

Adding commands is simple:

- create a file similar to the other files in the `project_automation.commands` directory;
- add it to the `__init__.py` file in the `project_automation.commands` module.

That's it!

---

### Add files

Adding files is simple:

- create a file similar to the other files in the `project_automation.files` folder;
- add it to the `__init__.py` file in the `project_automation.files` module.

That's it!

---

### Add projects

To add projects:

- create a file similar to the other files in the `project_automation.projects` folder;
- add it to the `__init__.py` file in the `project_automation.projects` module.
- add it to the argument parser, otherwise the project cannot be created.

If you decide to create a project on a language/framework not yet implemented, start by creating the commands and associated files. Then, simply create a module similar to the others in the `project_automation.projects` directory and repeat the above steps.

To choose the languages and framework used in the project, they are linked to the `gitignore` files available [here](https://github.com/github/gitignore).

If they are not there, just put the name of the language/framework used.

---

### Add licenses

To add license templates:

- create a file similar to the other files in the `project_automation.licenses` folder;
- add it to the `__init__.py` file in the `project_automation.licenses` module.
- add it to the `project_automation.settings` module in the `LICENSE_MODE` constant (to get the full name of the license type), then in `LICENSE_MODE_SHORTCUT` (to use it on the command line).
