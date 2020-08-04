"""Perform development installs of PyTorch"""
import os
import json
import subprocess

from .tools import timed


URL_FORMAT = "{base_url}/{platform}/{dist_name}.tar.bz2"


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
        else:
            deps.append(url)
    return deps, pytorch


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
    """"Install pytorch into the PWD"""
    cmd = ["conda", "create", "--yes", "--no-deps", "--prefix", ".", url]
    p = subprocess.run(cmd, check=True)



def install():
    """Development install of PyTorch"""
    deps, pytorch = conda_solve()
    deps_install(deps)
    pytorch_install(pytorch)
