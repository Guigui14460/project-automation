For Windows :

```shell
$ pyinstaller cli.py --exclude-module=autopep8 --hidden-import=pkg_resources.py2_warn --name automate_projects --onefile
```

For Unix-like systems :

```shell
$ pyinstaller cli.py --exclude-module=autopep8 --hidden-import=pkg_resources.py2_warn --name automate_projects --onefile
```
