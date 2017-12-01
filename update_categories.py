import os
import sys
import hugotools

def parse_args():
    argc = len(sys.argv)
    if argc == 2:
        return sys.argv[1]

    print("Invalid command args!")
    return None

if __name__ == "__main__":
    content_dir = parse_args()
    if not content_dir:
        print("Please specify hugo content dir !")
        sys.exit(1)

    tools = hugotools.HugoTools(content_dir)
    matched_files = tools.match_files(content_dir)
    for root, filename in matched_files:
        if tools.update_categories(root,filename):
            print "Update categories for: {0}".format(os.path.join(root, filename))
      
        
