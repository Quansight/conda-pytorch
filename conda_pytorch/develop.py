"""Perform development installs of PyTorch"""
import os
import json
import subprocess


URL_FORMAT = "{base_url}/{platform}/{dist_name}.tar.bz2"


def conda_solve():
    """Performs the conda solve and splits the deps from the package."""
    cmd = ["conda", "create", "--dry-run", "--json"
           "--name", "__pytorch__", "-c", "pytorch-nightly", "pytorch"]
    p = subprocess.run(cmd, capture_output=True, check=True)
    solve = json.loads(p.stdout)
    link = solve["actions"]["LINK"]
    deps = []
    for pkg in link:
        url = URL_FORMAT.format(**pkg)
        if pkg["name"] == "pytorch"
            pytorch = url
        else:
            deps.append(url)
    return deps, pytorch


def deps_install(deps):
    """Install dependencies to deps environment"""
    cmd = ["conda", "create", "--no-deps", "--name", "pytorch-deps"] + deps
    p = subprocess.run(cmd, check=True)


def pytorch_install(url):
    """"Install pytorch into the PWD"""
    cmd = ["conda", "create", "--no-deps", "--prefix", ".", url]
    p = subprocess.run(cmd, check=True)



def install():
    """Development install of PyTorch"""
    deps, pytorch = conda_solve()
    deps_install(deps)
    pytorch_install(pytorch)
