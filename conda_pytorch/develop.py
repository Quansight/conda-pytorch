"""Perform development installs of PyTorch"""
import os
import re
import json
import glob
import tempfile
import subprocess
from ast import literal_eval

from .tools import timed


URL_FORMAT = "{base_url}/{platform}/{dist_name}.tar.bz2"
SHA1_RE = re.compile("([0-9a-fA-F]{40})")
#GIT_VERSION_RE = re.compile(r"git_version\s*=\s*['\"]([0-9a-fA-F]+)['\"]")


@timed("Solving conda envrionment")
def conda_solve():
    """Performs the conda solve and splits the deps from the package."""
    cmd = ["conda", "create", "--yes", "--dry-run", "--json",
           "--name", "__pytorch__", "-c", "pytorch-nightly", "pytorch"]
    p = subprocess.run(cmd, capture_output=True, check=True)
    solve = json.loads(p.stdout)
    link = solve["actions"]["LINK"]
    deps = []
    for pkg in link:
        url = URL_FORMAT.format(**pkg)
        if pkg["name"] == "pytorch":
            pytorch = url
            platform = pkg["platform"]
        else:
            deps.append(url)
    return deps, pytorch, platform


@timed("Installing dependencies")
def deps_install(deps):
    """Install dependencies to deps environment"""
    # first remove previous env
    cmd = ["conda", "env", "remove", "--yes", "--name", "pytorch-deps"]
    p = subprocess.run(cmd, check=True)
    # install new deps
    cmd = ["conda", "create", "--yes", "--no-deps", "--name", "pytorch-deps"] + deps
    p = subprocess.run(cmd, check=True)


@timed("Installing pytorch nightly binaries")
def pytorch_install(url):
    """"Install pytorch into a temporary directory"""
    pytdir = tempfile.TemporaryDirectory()
    cmd = ["conda", "create", "--yes", "--no-deps", "--prefix", pytdir.name, url]
    p = subprocess.run(cmd, check=True)
    return pytdir


def _site_packages(pytdir):
    template = os.path.join(pytdir.name, "lib", "python*.*", "site-packages")
    spdir = glob.glob(template)[0]
    return spdir


@timed("Checking out nightly PyTorch")
def checkout_nightly_version(spdir):
    """Get's the nightly version and then checks it out."""
    # first get the git version from the installed module
    version_fname = os.path.join(spdir, "torch", "version.py")
    with open(version_fname) as f:
        lines = f.read().splitlines()
    for line in lines:
        if not line.startswith('git_version'):
            continue
        git_version = literal_eval(line.partition("=")[2].strip())
        break
    else:
        raise RuntimeError(f"Could not find git_version in {version_fname}")
    print(f"Found released git version {git_version}")
    # now cross refernce with nightly version
    cmd = ["git", "show", "--no-patch", "--format=%s", git_version]
    p = subprocess.run(cmd, capture_output=True, check=True, text=True)
    m = SHA1_RE.search(p.stdout)
    if m is None:
        raise RuntimeError(f"Could not find nightly release in git history:\n  {p.stdout}")
    nightly_version = m.group(1)
    print(f"Found nightly release version {nightly_version}")
    # now checkout nightly version
    cmd = ["git", "checkout", nightly_version]
    p = subprocess.run(cmd, check=True)


def _get_listing(source_dir, platform):
    system = platform.system()
    if platform.startswith("linux"):
        listing = _get_listing_linux(source_dir)
    elif platform.startswith("osx"):
        listing = _get_listing_osx(source_dir)
    elif platform.startswith("win"):
        listing = _get_listing_win(source_dir)
    else:
        raise RuntimeError(f"Platform {platform!r} not recognized")


@timed("Moving nightly files into repo")
def move_nightly_files(spdir, platform):
    source_dir = os.path.join(spdir, "torch")
    listing = _get_listing(source_dir, platform)
    target_dir = os.path.abspath("torch")


def install():
    """Development install of PyTorch"""
    deps, pytorch, platform = conda_solve()
    deps_install(deps)
    pytdir = pytorch_install(pytorch)
    spdir = _site_packages(pytdir)
    checkout_nightly_version(spdir)
    move_nightly_files(spdir, platform)
    pytdir.cleanup()
