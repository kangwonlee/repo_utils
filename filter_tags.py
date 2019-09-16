import argparse
import json
import subprocess
import sys
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


def main(argv):
    with open(argv[1], 'rt', encoding='utf-8') as fp:
        info_dict = json.load(fp)

    r_remote_list = add_remote_list(info_dict['url list'])
    r_fetch_all = git_fetch_all_tag()
    process_duplicate_tags()


if "__main__" == __name__:
    main(sys.argv)
