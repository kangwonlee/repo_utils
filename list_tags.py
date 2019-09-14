import pprint
import sys
import typing

import prefix_tags as pt


def main(argv: typing.List[str]) -> None:
    tag_list = pt.get_tag_list()

    tags_dict = {}
    for tag in tag_list:

        sha1 = pt.get_sha1(tag)

        sha_list = tags_dict.get(sha1, [])
        sha_list.append(tag)
        tags_dict[sha1] = sha_list

    pprint.pprint(tags_dict)


if "__main__" == __name__:
    main(sys.argv)
