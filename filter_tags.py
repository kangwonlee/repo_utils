import argparse
import configparser
import subprocess
import urllib.parse as up

import prefix_tags as pt


def add_remote(url:str, name:str=''):

    if not name:
        name = pt.get_repo_name_from_url(url)

    r = pt.run_cmd(
        ['git', 'remote', 'add', name, url]
    )

    return r


def git_fetch_all_tag():
    return pt.run_cmd(
        ['git', 'fetch', '--all', '--tag']
    )
