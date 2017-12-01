import os
import sys
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
    content_dir, taxonomy = parse_args()
    if not content_dir or not taxonomy:
        print("Please specify hugo content dir and taxonomy you want remove!")
        sys.exit(1)

    tools = hugotools.HugoTools(content_dir)
    matched_files = tools.match_files()
    for root, filename in matched_files:
        if tools.remove_taxonomy(root,filename, taxonomy):
            print "Removed taxonomy for: {0}".format(os.path.join(root, filename))
      
        
