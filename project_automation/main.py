import argparse
import inspect

from project_automation import projects, utils


def main():
    # Creation the base of the CLI parser
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-i', '--allow-install',
                        help='allows to install used commands/packages (False by default)', action='store_true', default=False)
    github_group = parser.add_argument_group(title='Github options')
    github_group.add_argument('--github', action='store_true',
                              help='use the github versioning')
    github_group.add_argument('--public', action='store_true',
                              help='make the github repo with "Public Status"')
    github_group.add_argument('--license', default='unlicense',
                              help='license type to add for the repo')

    # Sub-commands
    subparsers = parser.add_subparsers(
        help='Use one of the available sub-command', dest='command')

    modules = inspect.getmembers(projects, inspect.ismodule)
    parser_classes = []
    for _, module in modules:
        classes_in_module = inspect.getmembers(module, inspect.isclass)
        for _, Klass in list(filter(utils.get_parser_class, classes_in_module)):
            parser_classes.append(Klass(subparsers))

    # Get the CLI results
    result = parser.parse_args()

    # Creation of the arguments for the projects creation
    github_settings = {
        "public": result.public,
        "license": result.license,
    } if result.github else {}
    kwargs = {
        "klass": None,
        "path": result.path,
        "name": result.project_name,
        "github_settings": github_settings,
        "allow_install": result.allow_install,
    }

    # Iterate each parser class and get its key-word argument
    for parser_class in parser_classes:
        kwargs = parser_class.get_result(result, kwargs)

    # Generation of the project
    Klass = kwargs.pop('klass')
    if Klass != None:
        project = Klass(**kwargs)
        project.create()
        project.commit()
    else:
        raise ValueError("Any class project match with your command line")


if __name__ == "__main__":
    main()
