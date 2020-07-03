import os

from dotenv import load_dotenv

from .licenses import *

# Load the env file into the environment
load_dotenv()

# Get Github credentials
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_PASS = os.getenv("GITHUB_PASS")
GITHUB_OAUTH_ACCESS_TOKEN = os.getenv("GITHUB_OAUTH_ACCESS_TOKEN")

# License part
LICENSE_MODE = {
    "Apache License 2.0": apache2.CONTENT,
    "BSD 3-Clause \"New\" or \"Revised\" License": bsd3.CONTENT,
    "BSD 2-Clause \"Simplified\" License": bsd2.CONTENT,
    "Creative Commons Zero v1.0 Universal": cc1.CONTENT,
    "Eclipse Public License 2.0": eclipse2.CONTENT,
    "GNU General Public License v3.0": gnu3.CONTENT,
    "GNU General Public License v2.0": gnu2.CONTENT,
    "GNU Affero General Public License v3.0": gnu_affero3.CONTENT,
    "GNU Lesser General Public License v2.1": gnu_lesser21.CONTENT,
    "GNU Lesser General Public License v3.0": gnu_lesser3.CONTENT,
    "MIT License": mit.CONTENT,
    "Mozilla Public License 2.0": mozilla2.CONTENT,
    "Unlicense": unlicense.CONTENT,
}
LICENSE_MODE_SHORTCUT = {
    "apache": LICENSE_MODE['Apache License 2.0'],
    "bsd3": LICENSE_MODE['BSD 3-Clause "New" or "Revised" License'],
    "bsd2": LICENSE_MODE['BSD 2-Clause "Simplified" License'],
    "CC": LICENSE_MODE['Creative Commons Zero v1.0 Universal'],
    "eclipse": LICENSE_MODE['Eclipse Public License 2.0'],
    "gnu3": LICENSE_MODE['GNU General Public License v3.0'],
    "gnu2": LICENSE_MODE['GNU General Public License v2.0'],
    "gnuAffero3": LICENSE_MODE['GNU Affero General Public License v3.0'],
    "gnuLess3": LICENSE_MODE['GNU Lesser General Public License v3.0'],
    "gnuLess2.1": LICENSE_MODE['GNU Lesser General Public License v2.1'],
    "mit": LICENSE_MODE['MIT License'],
    "mozilla": LICENSE_MODE['Mozilla Public License 2.0'],
    "unlicense": LICENSE_MODE['Unlicense'],
}

SHELL_COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "endcolor": "\033[0m",
    "bold": "\033[1m",
    "underline": "\033[4m",
}
