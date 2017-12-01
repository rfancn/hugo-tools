import os
import re
import io
import datetime
import frontmatter
import traceback

class HugoTools(object):
    def __init__(self, content_dir, supported_languages=["zh", "en"]):
        self.content_dir = content_dir
        if not self.content_dir:
            raise Exception("Empty content dir")

        self.supported_languages = supported_languages
        self.section_index_files = set(["_index.{0}.md".format(lang) for lang in self.supported_languages])
        self.regex_contains_chinese_text = re.compile(ur'[\u4e00-\u9fff]+')
        self.regex_is_index_file = re.compile(r'index.*.md')
        self.front_matter = None
        self.absfile = None

    def match_files(self, exclude_regex=None):
        matched = []

        filename_match_regex = None
        if exclude_regex:
            try:
                filename_match_regex = re.compile(exclude_regex)
            except:
                print("Invalid exclude regular expression specified!")
                return None, None

        for root, dirs, files in os.walk(self.content_dir):
            for filename in files:
                # ignore files matched exclude regular expression
                if filename_match_regex and filename_match_regex.match(filename):
                    continue

                if filename.endswith(".md"):
                    matched.append((root, filename))

        return matched


    def init_nested_sections(self):
        """
        To display the list of pages under section,
        it need at least create a _index.md for all languages
        under one of the most deeply nested directory

        when access the url of a nested section:
        1. if it contains index.*.md:  shows the content of index.*.md
        2. no index.*.md, but contains _index.*.md: shows the list of all post files under this dir
        3. no index.*.md, no _index.*.md:  shows nothing
        """
        # the most deeply nested dir
        def find_nested_sections(content_dir):
            for root, dirs, files in os.walk(content_dir):
                # ignore the content dir
                if root == content_dir:
                    continue

                if is_post_dir(files):
                    continue

                yield root, files

        # check if a dir contains index.*.md files or not,
        # if yes, then access the url of that dir will show the content of the post
        def is_post_dir(files):
            for filename in files:
                if self.regex_is_index_file.match(filename):
                    return True

            return False


        for root, files in find_nested_sections(self.content_dir):
            # in case, current files doesn't contains all language index files
            if not self.section_index_files.issubset(set(files)):
                print "Initilize section: {0}".format(root)
                for f in self.section_index_files:
                    target_index_file = os.path.join(root, f)
                    try:
                        open(target_index_file, 'a').close()
                    except:
                        print "Failed to create {0} under {1}".format(f, root)
                        return False

    def get_lang_code(self, root, filename):
        absfile = os.path.join(root, filename)
        with io.open(absfile, "r", encoding='utf8') as f:
            file_content = f.read()

            if self.regex_contains_chinese_text.findall(file_content):
                return "zh"

        return "en"

    def rename_with_lang(self, root, filename):
        if filename in self.section_index_files:
            return ""

        file_lang_code = self.get_lang_code(root, filename)

        name_list = filename.split(".")
        part_num = len(name_list)
        # for files only have one ".", insert file_lang_code directly
        if part_num == 2:
            new_filename = "{0}.{1}.md".format(name_list[0], file_lang_code)
        elif part_num == 1:
            print "invalid filename"
            return ""
        elif part_num > 2:
            maybe_lang = name_list[-2]
            if maybe_lang == file_lang_code:
                # Skipped rename as it already contains langcode
                return ""
            else:
                first_part =  ".".join(name_list[:-1])
                new_filename = "{0}.{1}.md".format(first_part, file_lang_code)

        orig_file = os.path.join(root, filename)
        target_file = os.path.join(root, new_filename)

        try:
            os.rename(orig_file, target_file)
        except:
            print "Failed to rename file:{0} to lang:{1}".format(filename, file_lang_code)
            traceback.print_exc()
            return ""

        return new_filename

    def remove_taxonomy(self, root, filename, taxonomy, auto_save=True):
        if not self.read_frontmatter(root, filename):
            return False

        try:
            term_list = taxonomy.split(",")
            for term in term_list:
                term = term.strip()
                del self.front_matter[term]
        except KeyError:
            return False
        except Exception as ex:
            print "Error remove taxonomy for file:{0}".format(filename)
            traceback.print_exc()
            return False

        if auto_save:
            if not self.save_frontmatter():
                return False

        return True


    def read_frontmatter(self, root, filename):
        current_absfile = os.path.join(root, filename)
        if self.absfile == current_absfile:
            if self.front_matter:
                return True

        self.absfile = current_absfile
        if not os.path.isfile(self.absfile):
            print("Failed to read frontmatter file: {0}".format(self.absfile))
            return False

        try:
            self.front_matter = frontmatter.load(self.absfile)
        except Exception as ex:
            print "Failed to read frontmatter from file:{0}".format(self.absfile)
            traceback.print_exc()
            return False

        return True

    def save_frontmatter(self):
        try:
            frontmatter.dump(self.front_matter, self.absfile, allow_unicode=True)
        except Exception as ex:
            print "Error save frontmatter for file:{0}".format(self.absfile)
            traceback.print_exc()
            return False

        return True

    def update_lastmod(self, root, filename, auto_save=True):
        if not self.read_frontmatter(root, filename):
            return False

        try:
            self.front_matter["lastmod"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except KeyError:
            return False
        except:
            print "Error update lastmod for file:{0}".format(self.absfile)
            traceback.print_exc()
            return False

        if auto_save:
            if not self.save_frontmatter():
                return False

        return True

    def turn_off_draft(self, root, filename, auto_save=True):
        if not self.read_frontmatter(root, filename):
            return False

        try:
            self.front_matter["draft"] = False
        except KeyError:
            return False
        except:
            print "Error turn off draft for file:{0}".format(self.absfile)
            traceback.print_exc()
            return False

        if auto_save:
            if not self.save_frontmatter():
                return False

        return True

    def update_categories(self, root, filename, auto_save=True):
        if not self.read_frontmatter(root, filename):
            return False

        try:
            self.front_matter["categories"] = os.path.relpath(root, self.content_dir).split("/")
        except KeyError:
            return False
        except:
            print "Error update categories for file:{0}".format(self.absfile)
            traceback.print_exc()
            return False

        if auto_save:
            if not self.save_frontmatter():
                return False

        return True

    def publish(self, root, filename):
        self.init_nested_sections()

        if not self.read_frontmatter(root, filename):
            return False, ""

        #1. Ignore those pages with draft=True flag
        draft = self.front_matter.get("draft", False)
        if draft is True:
            print("Skip publish: {0} as it is a draft.".format(os.path.join(root, filename)))
            return False, ""

        #2 update current categories
        #frontmatter_categories = self.front_matter.get("categories", [])
        #current_categories = os.path.relpath(root, self.content_dir).split("/")
        #if frontmatter_categories and set(frontmatter_categories) != set(current_categories):
        #    if not self.update_categories(root,filename, auto_save=False):
        #        print("Publish[{0}]: Failed to turn off draft.".format(filename))
        #        return False, ""
        #    else:
        #        changed = True
        # changed = middle_operations()
        changed = False

        #3. update latstmod and save it
        if changed:
            if not self.update_lastmod(root,filename):
                print("Publish[{0}]: Failed to update last modification time.".format(filename))
                return False, ""

        #4. add lang suffix to post files
        publish_filename = self.rename_with_lang(root, filename)

        return changed, publish_filename




