import argparse
import os
import subprocess
import sys
import typing
import urllib.parse as up


def main(argv: typing.List[str]) -> None:

    p = get_argparse()
    ns = p.parse_args(argv[1:])
    
    tag_list = get_tag_list()

    for tag in tag_list:
        if not tag.startswith(ns.prefix):
            handle_tag(tag, ns)


def handle_tag(tag: str, ns: argparse.Namespace) -> None:
    sha1 = get_sha1(tag)
    if ns.dry_run:
        print(sha1, tag)
        print(f'git tag {ns.prefix}/{tag} {tag}')
        print(f'git tag --delete {tag}')
        print(f'git push {ns.remote} --delete {tag}')
    else:
        print(sha1, tag)

        print(f'git tag {ns.prefix}/{tag} {tag}')
        r_set_tag = set_tag('/'.join([ns.prefix,tag]), tag)
        print(r_set_tag.stdout)
        print(r_set_tag.stderr)

        print(f'git tag --delete {tag}')

        r_remove = remove_tag_local_remote(tag, ns.remote)
        print(r_remove['local'].stdout)
        print(r_remove['local'].stderr)

        print(f'git push {ns.remote} --delete {tag}')
        print(r_remove['remote'].stdout)
        print(r_remove['remote'].stderr)


def get_argparse() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog='rename tag',
    )

    p.add_argument('prefix', type=str, help="desired prefix")
    p.add_argument('--remote', type=str, default="origin", help="remote repository")
    p.add_argument('--dry-run', action='store_true', default=False)

    return p


def get_repo_name(remote):

    result = ''

    r = subprocess.check_output(
        ['git', 'remote', '-v'],
        encoding='utf-8',
    )

    for line in r.stdout.splitlines():
        ls = line.split()
        if ls[0] == remote:
            parse = up.urlparse(ls[1])
            result = os.path.split(parse.path)[-1]
            break

    return result


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
        ['git', 'log', '-1', '--pretty=format:%H', ref],
        capture_output=True,
        encoding='utf-8',
        check=True,
    )

    return r.stdout.strip()


if "__main__" == __name__:
    main(sys.argv)
