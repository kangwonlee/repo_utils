import argparse
import configparser
import subprocess
import typing
import urllib.parse as up

import list_tags as lt
import prefix_tags as pt


def add_remote(url:str, name:str=''):
    if not name:
        name = pt.get_repo_name_from_url(url)

    r = pt.run_cmd(
        ['git', 'remote', 'add', name, url]
    )

    return r


def add_remote_list(remote_url_list:typing.List[str]):
    return [add_remote(url)  for url in remote_url_list]


def git_fetch_all_tag():
    return pt.run_cmd(
        ['git', 'fetch', '--all', '--tag']
    )


def process_duplicate_tags():
    lt.main([])
