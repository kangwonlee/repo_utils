import argparse
import os
import subprocess
import sys
import typing
import urllib.parse as up


ShellCommand = typing.Union[str, typing.List[str]]


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
            result = get_repo_name_from_url(ls[1])
            break

    return result


def get_repo_name_from_url(url:str) -> str:
    parse = up.urlparse(url)
    path_split = os.path.split(parse.path)

    result = path_split[-1]

    del path_split
    del parse

    return result


def set_tag(new_tag, ref):
    r = run_cmd(['git', 'tag', new_tag, ref])

    return r


def remove_tag_local_remote(tag:str, remote:str) -> typing.Dict[str, subprocess.CompletedProcess]:
    r_remote = run_cmd(
        ['git', 'push', remote, '--delete', tag], 
        check=False,
    )
    r_local = git_delete_tag_local(tag)

    return {'remote': r_remote, 'local': r_local}


def git_delete_tag_local(tag):
    return run_cmd(
        ['git', 'tag', '--delete', tag], 
        check=False,
    )


def get_tag_list()-> typing.List[str]:
    r_tags = run_cmd(['git', 'tag'])

    return [tag.strip() for tag in r_tags.stdout.splitlines()]


def get_sha1(ref: str) -> str:

    r = run_cmd(
        ['git', 'log', '-1', '--pretty=format:%H', ref]
    )

    return r.stdout.strip()


def run_cmd(cmd: ShellCommand, check:bool=True, capture_output:bool=True, encoding:str='utf-8') -> subprocess.CompletedProcess:
    completed_process = subprocess.run(
        cmd,
        capture_output=True,
        encoding='utf-8',
        check=check,
    )

    return completed_process


if "__main__" == __name__:
    main(sys.argv)
