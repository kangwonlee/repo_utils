import argparse
import subprocess
import sys
import typing


def main(argv):

    p = get_argparse()
    ns = p.parse_args(argv[1:])
    
    tag_list = get_tag_list()

    for tag in tag_list:
        if not tag.startswith(ns.prefix):
            sha1 = get_sha1(tag)
            print(sha1, tag)


def get_argparse() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()

    p.add_argument('--prefix', type=str, required=True)

    return p


def set_tag(new_tag, ref):
    r = subprocess.run(
        ['git', 'tag', new_tag, ref],
        capture_output=True,
        encoding='utf-8',
        check=True,
    )

    return r


def remove_tag_local_remote(tag:str, remote:str) -> typing.Dict[str, subprocess.CompletedProcess]:
    r_remote = subprocess.run(
        ['git', 'push', remote, '--delete', tag], 
        capture_output=True,
        encoding='utf-8',
        check=True,
    )
    r_local = subprocess.run(
        ['git', 'tag', '--delete', tag], 
        capture_output=True,
        encoding='utf-8',
        check=True,
    )

    return {'remote': r_remote, 'local': r_local}


def get_tag_list()-> typing.List[str]:
    r_tags = subprocess.run(
        ['git', 'tag'],
        capture_output=True,
        encoding='utf-8',
        check=True,
    )

    return [tag.strip() for tag in r_tags.stdout.splitlines()]


def get_sha1(ref: str) -> str:
    r = subprocess.run(
        ['git', 'show', '--pretty=format:%H', ref],
        capture_output=True,
        encoding='utf-8',
        check=True,
    )

    return r.stdout.strip()


if "__main__" == __name__:
    main(sys.argv)
