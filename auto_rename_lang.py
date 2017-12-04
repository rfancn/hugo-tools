import sys
import os
import hugotools

def parse_args():
    argc = len(sys.argv)
    if argc == 2:
        return sys.argv[1], None
    elif argc == 3:
        return sys.argv[1], sys.argv[2]

    print("Invalid command args!")
    return None, None



if __name__ == "__main__":
    content_dir, config_file = parse_args()

    tools = hugotools.HugoTools(content_dir, config_file)
    matched_files = tools.match_files()
    #for root, filename in matched_files:
    #    tools.rename_with_lang(root, filename)
