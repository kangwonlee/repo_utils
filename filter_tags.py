import argparse
import json
import os
import subprocess
import sys
import typing
import urllib.parse as up


import list_tags as lt
import prefix_tags as pt


PrefixList = typing.Union[typing.List[str], typing.Set[str], typing.Tuple[str]]


def add_remote(url:str, name:str=''):
    if not name:
        name = pt.get_repo_name_from_url(url)

    r = pt.run_cmd(
        ['git', 'remote', 'add', name, url]
    )

    return r


def remove_remote(name:str='', url:str=''):
    """
    name would override url
    """
    if not name and not url:
        raise ValueError('need either url or name')

    if not name and url:
        name = pt.get_repo_name_from_url(url)

    r = pt.run_cmd(
        ['git', 'remote', 'remove', name]
    )

    return r


def add_remote_list(remote_url_list:typing.List[str]):
    return [add_remote(url)  for url in remote_url_list]


def remove_remote_list(remote_url_list:typing.List[str]):
    return [remove_remote(url=url)  for url in remote_url_list]


def git_fetch_all_tag():
    return pt.run_cmd(
        ['git', 'fetch', '--all', '--tag']
    )


def process_duplicate_tags():
    lt.main([])


def get_repo_name_list(url_list:typing.List[str]) -> typing.List[str]:
    return [pt.get_repo_name_from_url(url) for url in url_list]


def get_tag_prefix(tag:str) -> str:
    tag_split_list = tag.split('/')

    result = tag_split_list[0]

    del tag_split_list

    return result


def main(argv):
    if 2 > len(argv) :
        print('Please give a json file name')
        sys.exit(-1)
    elif os.path.exists(argv[1]):
        json_filename = argv[1]
    else:
        json_filename = os.path.join(
            os.path.dirname(__file__),
            argv[1]
        )

    assert os.path.exists(json_filename), json_filename

    with open(json_filename, 'rt', encoding='utf-8') as fp:
        info_dict = json.load(fp)

    repo_name_list = get_repo_name_list(info_dict['url list'])

    r_remote_list = add_remote_list(info_dict['url list'])
    r_fetch_all = git_fetch_all_tag()
    process_duplicate_tags()
    r_remove_list = remove_remote_list(info_dict['url list'])
    # TODO : remove tags with different prefixes


if "__main__" == __name__:
    main(sys.argv)
