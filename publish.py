import sys
import hugotools
import os

def parse_args():
    argc = len(sys.argv)
    if argc == 2:
        return sys.argv[1], None
    elif argc == 3:
        return sys.argv[1], sys.argv[2]

    print("Invalid command args!")
    return None, None

if __name__ == "__main__":
    content_dir, exclude_regex = parse_args()
    if not content_dir:
        print("Please input content dir!")
        sys.exit(1)

    tools = hugotools.HugoTools(content_dir)
    matched_files = tools.match_files(exclude_regex)
    for root, filename in matched_files:
        changed, publish_filename = tools.publish(root, filename)
        if publish_filename:
            print "Auto rename file: {0} to contains language suffix".format(os.path.join(root,filename))

        if changed:
            print "Successfully publish: {0}".format(os.path.join(root, publish_filename))
