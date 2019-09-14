import pprint
import sys
import typing

import prefix_tags as pt

Tags = typing.List[str]
Sha_Tags = typing.Dict[str, Tags]


def main(argv: typing.List[str]) -> None:
    sha_tags_dict = get_sha_tags_dict()

    duplicate_sha_tags = filter_duplicate_tags(sha_tags_dict)

    pprint.pprint(duplicate_sha_tags)


def remove_duplicate_tags(duplicate_sha_tags: Sha_Tags):
    for tags in duplicate_sha_tags.values():
        for tag in tags:
            pt.remove_tag_local_remote(tag, 'origin')


def filter_duplicate_tags(sha_tags_dict:Sha_Tags) -> Sha_Tags:
    return {
        key: value for key, value in filter(
            lambda sha_tags: 1 < len(sha_tags[-1]),
            sha_tags_dict.items()
        )
    }


def get_sha_tags_dict() -> Sha_Tags:
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
