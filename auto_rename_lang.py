import sys
import os
import hugotools

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify hugo content dir!")
        sys.exit(1)

    content_dir = sys.argv[1]
    tools = hugotools.HugoTools(content_dir)
    matched_files = hugotools.match_files(content_dir)
    for root, filename in matched_files:
        tools.rename_with_lang(root, filename)
