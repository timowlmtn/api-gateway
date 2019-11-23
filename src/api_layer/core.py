# -*- coding: utf-8 -*-

import re


def parse_regexp(regexp, string, json_key_list):
    """
    Parse a regular expression and return the result as dictionary object

    :param regexp:  A regular expression to parse
    :param string:  A string to parse
    :param json_key_list: A list of JSON keys to extract from the regular expression and return
    :param ignore_case: Default to ignore case
    :return:
    """
    match = re.match(regexp, string)
    list_iter = iter(json_key_list)
    result = dict()
    default_key = 0
    if match:
        for group_val in match.groups():
            json_key = next(list_iter)
            if json_key:
                result[json_key] = group_val
            else:
                result[f"GROUP_{default_key}"] = group_val
                default_key = default_key + 1

    return result
