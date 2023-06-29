def custom_tag_string_parser(tag_string):
    return [t.strip(' "') for t in tag_string.split(",") if t.strip(' "')]
