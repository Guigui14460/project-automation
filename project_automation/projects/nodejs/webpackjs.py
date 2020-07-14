import os
from typing import Any, NoReturn

from project_automation.commands import TypescriptCommand
from project_automation.files import Folder, HTMLFile, CSSFile, SASSFile, JavascriptFile, TypescriptFile
from project_automation.projects.nodejs.nodejs import NodeJSProject
from project_automation.utils import execute_command2, read_from_json_file, write_in_json_file


class WebpackJSProject(NodeJSProject):
    """
    Represents the base of WebpackJS project to create.

    Attributes
    ----------
    path : str
        path of the parent root of the project
    name : str
        name of the project (used for make directory and github repo)
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    github_settings : dict
        some github informations
    errors : list of string
        all occured error during project creation (not exceptions)
    user : ~github.AuthenticatedUser or ~github.NamedUser
        github user if ``github_settings`` is not empty
    root : ~files.Folder
        root folder of the project
    npm_version : tuple of strings
        npm version
    """

    CONFIG = {
        'languages': ["WebpackJS", "Javascript", "Node"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ('code', '$ npm start', 'shell'),
        }
    }

    def __init__(self, path: str, name: str, github_settings: dict = {}, **kwargs: Any) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the parent root of the project
        name : str
            name of the project (used for make directory and github repo)
        github_settings : dict
            some github informations
        **kwargs : Any
            other keywords parameters
        """
        super().__init__(path, name,
                         github_settings=github_settings, **kwargs)

    def create(self) -> NoReturn:
        """
        Create the structure of the project.

        See also
        --------
        utils.execute_command2
        """
        sass = 'y' in input(
            "Do you want to include Sass/Scss files ? (y/n) ").lower()
        ts = 'y' in input(
            "Do you want to include TypeScript files ? (y/n) ").lower()
        super().create()
        os.chdir(self.path)
        source_folder_path = os.path.join(self.path, "src")
        source_folder = Folder(source_folder_path)
        self.root.add(Folder(os.path.join(self.path, "public")), source_folder)
        if self.allow_install:
            execute_command2(
                'npm i -D webpack webpack-cli webpack-dev-server @babel/core babel-loader @babel/preset-env html-webpack-plugin html-loader file-loader style-loader css-loader mini-css-extract-plugin')
            package_json = read_from_json_file(
                os.path.join(self.path, 'package.json'))
            package_json['scripts'] = {
                "build": "webpack --mode=production",
                "start": "webpack-dev-server"
            }
            write_in_json_file(os.path.join(
                self.path, 'package.json'), package_json, indent_json=2)
            if sass:
                execute_command2("npm i -D node-sass sass-loader webpack-sass")
            if ts:
                execute_command2("npm i -D ts-loader typescript")
                execute_command2('tsc --init')
                print("Finally, change target by \"es6\" and module by \"es2015\"")
        else:
            print('Launch this command `npm i -D webpack webpack-cli webpack-dev-server @babel/core babel-loader @babel/preset-env`')
            print("Change the 'scripts' part of the package.json file :")
            print("- build value : webpack --mode=production")
            print("- start value : webpack-dev-server")
            print("Execute the following commands :")
            print("\tnpm i -D html-webpack-plugin html-loader file-loader")
            print("\tnpm i -D style-loader css-loader mini-css-extract-plugin")
            if sass:
                print("\tnpm i -D node-sass sass-loader webpack-sass")
            if ts:
                print("\tnpm i -D ts-loader typescript")
                print("\ntsc --init")
                print("Finally, change target by \"es6\" and module by \"es2015\"")
        ts_content = """{
        test: /\.tsx?$/,
        include: [path.resolve(__dirname, "src")],
        use: "ts-loader",
        exclude: /node_modules/,
      },"""
        ts_resolve = """".tsx", ".ts","""
        sass_content = """{
        test: /\.scss$/,
        include: [path.resolve(__dirname, "src")],
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },"""
        webpack_config_content = f"""const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {{
  mode: "development", // development or production
  devtool: "eval-source-map",
  entry: "./src/app.js",
  module: {{
    rules: [
      {{
        test: /\.jsx?$/,
        exclude: /node_modules/,
        include: [path.resolve(__dirname, "src")],
        use: "babel-loader",
      }},
      {ts_content if ts else ''}
      {{
        test: /\.css$/,
        include: [path.resolve(__dirname, "src")],
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
        ],
      }},
      {sass_content if sass else ''}
      {{
        test: /\.html$/,
        include: [path.resolve(__dirname, "src")],
        use: [
          {{
            loader: "html-loader",
            options: {{ minimize: true }},
          }},
        ],
      }},
      {{
        test: /\.(png|svg|jpg|jpeg|gif)$/,
        include: [path.resolve(__dirname, "src")],
        use: "file-loader",
      }},
    ],
  }},
  resolve: {{ extensions: [{ts_resolve if ts else ''}".jsx", ".js"] }},
  plugins: [
    new HtmlWebpackPlugin({{
      filename: "index.html",
      template: "src/index.html",
    }}),
    new MiniCssExtractPlugin({{
      filename: "index.css",
    }}),
  ],
  output: {{
    filename: "app.bundle.js",
    path: path.resolve(__dirname, "public"),
  }},
}};
"""
        webpack_config = JavascriptFile(self.path, 'webpack.config')
        webpack_config.write(webpack_config_content)
        self.root.add(webpack_config)

        assets_dir = Folder(os.path.join(source_folder_path, "assets"))
        images_dir = Folder(os.path.join(
            os.path.join(source_folder_path, "assets"), "images"))
        fonts_dir = Folder(os.path.join(
            os.path.join(source_folder_path, "assets"), "fonts"))
        assets_dir.add(images_dir, fonts_dir)
        source_folder.add(assets_dir)

        css_dir = Folder(os.path.join(source_folder_path, "styles"))
        if sass:
            style = SASSFile(os.path.join(
                source_folder_path, "styles"), "main")
        else:
            style = CSSFile(os.path.join(
                source_folder_path, "styles"), "style")
        css_dir.add(style)
        source_folder.add(css_dir)

        if ts:
            main_ts = TypescriptFile(source_folder_path, 'main')
            main_ts.write("export const perfect: string = \"perfect\";\n")
            source_folder.add(main_ts)
        app_js = JavascriptFile(source_folder_path, 'app')
        app_js.write(f"""{"import './styles/main.scss';" if sass else "import './styles/style.css';"}
import {{ bro }} from "./bro";
{"import { perfect } from './main';" if ts else ''}

let ok = ["ok", "ok"];
console.log(ok);
console.log(bro("Dude"));
{"console.log(perfect);" if ts else ''}
""")
        bro_js = JavascriptFile(source_folder_path, 'bro')
        bro_js.write("""export const bro = (greeting) => {
  return `${greeting}, bro`;
};
""")
        source_folder.add(bro_js, app_js, HTMLFile(
            source_folder_path, 'index'))

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        commands.TypescriptCommand
        """
        super().verify_installation()
        TypescriptCommand(self.allow_install)
