import pprint
import sys
import typing

import prefix_tags as pt


def main(argv: typing.List[str]) -> None:

    sha_tags_dict = get_sha_tags_dict()
    pprint.pprint(sha_tags_dict)


def get_sha_tags_dict():
    tag_list = pt.get_tag_list()

    tags_dict = {}
    for tag in tag_list:

        sha1 = pt.get_sha1(tag)

        sha_list = tags_dict.get(sha1, [])
        sha_list.append(tag)
        tags_dict[sha1] = sha_list

    return tags_dict


if "__main__" == __name__:
    main(sys.argv)
