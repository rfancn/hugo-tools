# coding: utf8

import os
import re
import io
import datetime
import frontmatter
import traceback
import subprocess

LANGUAGES = [
    ('aa', 'Afar'),
    ('ab', 'Abkhazian'),
    ('af', 'Afrikaans'),
    ('ak', 'Akan'),
    ('sq', 'Albanian'),
    ('am', 'Amharic'),
    ('ar', 'Arabic'),
    ('an', 'Aragonese'),
    ('hy', 'Armenian'),
    ('as', 'Assamese'),
    ('av', 'Avaric'),
    ('ae', 'Avestan'),
    ('ay', 'Aymara'),
    ('az', 'Azerbaijani'),
    ('ba', 'Bashkir'),
    ('bm', 'Bambara'),
    ('eu', 'Basque'),
    ('be', 'Belarusian'),
    ('bn', 'Bengali'),
    ('bh', 'Bihari languages'),
    ('bi', 'Bislama'),
    ('bo', 'Tibetan'),
    ('bs', 'Bosnian'),
    ('br', 'Breton'),
    ('bg', 'Bulgarian'),
    ('my', 'Burmese'),
    ('ca', 'Catalan; Valencian'),
    ('cs', 'Czech'),
    ('ch', 'Chamorro'),
    ('ce', 'Chechen'),
    ('zh', 'Chinese'),
    ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'),
    ('cv', 'Chuvash'),
    ('kw', 'Cornish'),
    ('co', 'Corsican'),
    ('cr', 'Cree'),
    ('cy', 'Welsh'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('de', 'German'),
    ('dv', 'Divehi; Dhivehi; Maldivian'),
    ('nl', 'Dutch; Flemish'),
    ('dz', 'Dzongkha'),
    ('el', 'Greek, Modern (1453-)'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('eu', 'Basque'),
    ('ee', 'Ewe'),
    ('fo', 'Faroese'),
    ('fa', 'Persian'),
    ('fj', 'Fijian'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('fr', 'French'),
    ('fy', 'Western Frisian'),
    ('ff', 'Fulah'),
    ('Ga', 'Georgian'),
    ('de', 'German'),
    ('gd', 'Gaelic; Scottish Gaelic'),
    ('ga', 'Irish'),
    ('gl', 'Galician'),
    ('gv', 'Manx'),
    ('el', 'Greek, Modern (1453-)'),
    ('gn', 'Guarani'),
    ('gu', 'Gujarati'),
    ('ht', 'Haitian; Haitian Creole'),
    ('ha', 'Hausa'),
    ('he', 'Hebrew'),
    ('hz', 'Herero'),
    ('hi', 'Hindi'),
    ('ho', 'Hiri Motu'),
    ('hr', 'Croatian'),
    ('hu', 'Hungarian'),
    ('hy', 'Armenian'),
    ('ig', 'Igbo'),
    ('is', 'Icelandic'),
    ('io', 'Ido'),
    ('ii', 'Sichuan Yi; Nuosu'),
    ('iu', 'Inuktitut'),
    ('ie', 'Interlingue; Occidental'),
    ('ia', 'Interlingua (International Auxiliary Language Association)'),
    ('id', 'Indonesian'),
    ('ik', 'Inupiaq'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('jv', 'Javanese'),
    ('ja', 'Japanese'),
    ('kl', 'Kalaallisut; Greenlandic'),
    ('kn', 'Kannada'),
    ('ks', 'Kashmiri'),
    ('ka', 'Georgian'),
    ('kr', 'Kanuri'),
    ('kk', 'Kazakh'),
    ('km', 'Central Khmer'),
    ('ki', 'Kikuyu; Gikuyu'),
    ('rw', 'Kinyarwanda'),
    ('ky', 'Kirghiz; Kyrgyz'),
    ('kv', 'Komi'),
    ('kg', 'Kongo'),
    ('ko', 'Korean'),
    ('kj', 'Kuanyama; Kwanyama'),
    ('ku', 'Kurdish'),
    ('lo', 'Lao'),
    ('la', 'Latin'),
    ('lv', 'Latvian'),
    ('li', 'Limburgan; Limburger; Limburgish'),
    ('ln', 'Lingala'),
    ('lt', 'Lithuanian'),
    ('lb', 'Luxembourgish; Letzeburgesch'),
    ('lu', 'Luba-Katanga'),
    ('lg', 'Ganda'),
    ('mk', 'Macedonian'),
    ('mh', 'Marshallese'),
    ('ml', 'Malayalam'),
    ('mi', 'Maori'),
    ('mr', 'Marathi'),
    ('ms', 'Malay'),
    ('Mi', 'Micmac'),
    ('mk', 'Macedonian'),
    ('mg', 'Malagasy'),
    ('mt', 'Maltese'),
    ('mn', 'Mongolian'),
    ('mi', 'Maori'),
    ('ms', 'Malay'),
    ('my', 'Burmese'),
    ('na', 'Nauru'),
    ('nv', 'Navajo; Navaho'),
    ('nr', 'Ndebele, South; South Ndebele'),
    ('nd', 'Ndebele, North; North Ndebele'),
    ('ng', 'Ndonga'),
    ('ne', 'Nepali'),
    ('nl', 'Dutch; Flemish'),
    ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian'),
    ('nb', 'Bokmål, Norwegian; Norwegian Bokmål'),
    ('no', 'Norwegian'),
    ('oc', 'Occitan (post 1500)'),
    ('oj', 'Ojibwa'),
    ('or', 'Oriya'),
    ('om', 'Oromo'),
    ('os', 'Ossetian; Ossetic'),
    ('pa', 'Panjabi; Punjabi'),
    ('fa', 'Persian'),
    ('pi', 'Pali'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('ps', 'Pushto; Pashto'),
    ('qu', 'Quechua'),
    ('rm', 'Romansh'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('rn', 'Rundi'),
    ('ru', 'Russian'),
    ('sg', 'Sango'),
    ('sa', 'Sanskrit'),
    ('si', 'Sinhala; Sinhalese'),
    ('sk', 'Slovak'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('se', 'Northern Sami'),
    ('sm', 'Samoan'),
    ('sn', 'Shona'),
    ('sd', 'Sindhi'),
    ('so', 'Somali'),
    ('st', 'Sotho, Southern'),
    ('es', 'Spanish; Castilian'),
    ('sq', 'Albanian'),
    ('sc', 'Sardinian'),
    ('sr', 'Serbian'),
    ('ss', 'Swati'),
    ('su', 'Sundanese'),
    ('sw', 'Swahili'),
    ('sv', 'Swedish'),
    ('ty', 'Tahitian'),
    ('ta', 'Tamil'),
    ('tt', 'Tatar'),
    ('te', 'Telugu'),
    ('tg', 'Tajik'),
    ('tl', 'Tagalog'),
    ('th', 'Thai'),
    ('bo', 'Tibetan'),
    ('ti', 'Tigrinya'),
    ('to', 'Tonga (Tonga Islands)'),
    ('tn', 'Tswana'),
    ('ts', 'Tsonga'),
    ('tk', 'Turkmen'),
    ('tr', 'Turkish'),
    ('tw', 'Twi'),
    ('ug', 'Uighur; Uyghur'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('ve', 'Venda'),
    ('vi', 'Vietnamese'),
    ('vo', 'Volapük'),
    ('cy', 'Welsh'),
    ('wa', 'Walloon'),
    ('wo', 'Wolof'),
    ('xh', 'Xhosa'),
    ('yi', 'Yiddish'),
    ('yo', 'Yoruba'),
    ('za', 'Zhuang; Chuang'),
    ('zh', 'Chinese'),
    ('zu', 'Zulu')
]

class HugoTools(object):
    def __init__(self, content_dir, config_file=None):
        self.content_dir = content_dir
        self.config_file = config_file

        if not self.content_dir:
            raise Exception("Empty content dir!")

        if not self.setup_lanagues():
            raise Exception("no language setting, you may not specify the config file")

        self.regex_contains_chinese_text = re.compile(ur'[\u4e00-\u9fff]+')
        self.regex_is_index_file = re.compile(r'index.*.md')
        self.front_matter = None
        self.absfile = None

    def setup_lanagues(self):
        self.lang_codes = [ lang_tuple[0] for lang_tuple in LANGUAGES ]

        # get default language, and supported lanagues
        self.default_lang, self.lang_list = self.get_languages()
        if self.default_lang is None or self.lang_list is None:
            return False

        # set section index files based on above
        if len(self.lang_list) > 1:
            self.section_index_files_set = set(["_index.{0}.md".format(lang) for lang in self.lang_list])
        else:
            self.section_index_files_set = set(["_index.md"])

        return True

    def get_languages(self):
        cmd_default_lang = "hugo config | grep defaultcontentlanguage:"
        cmd_all_lang = "hugo config | grep languagessorted:"
        if self.config_file:
            cmd_default_lang = "hugo config --config {0} | grep defaultcontentlanguage:".format(self.config_file)
            cmd_all_lang = "hugo config --config {0}| grep languagessorted:".format(self.config_file)

        try:
            FNULL = open(os.devnull, 'w')
            output_all_lang = subprocess.check_output(cmd_all_lang, stderr=FNULL, shell=True)
            output_default_lang = subprocess.check_output(cmd_default_lang, stderr=FNULL, shell=True)
        except subprocess.CalledProcessError as ex:
            print("Failed to check languages: %s" % ex)
            return None, None
        except Exception as ex:
            print("Failed to check languages")
            traceback.print_exc()
            return None, None

        try:
            default_lang = re.findall(r'defaultcontentlanguage: \"(.*)\"', output_default_lang)[0]
            all_lang = re.findall(r'languagessorted: \[(.*)\]', output_all_lang)[0]
            lang_list = all_lang.split(" ")
        except Exception as ex:
            print("Failed to parse languages")
            traceback.print_exc()
            return None, None

        return default_lang, lang_list

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

        try:
            self.section_index_files_set
        except AttributeError:
            print("Initialize section doesnt' work")
            return False
        else:
            for root, files in find_nested_sections(self.content_dir):
                # get current index files set
                current_index_files_set = set([ f for f in files if f.startswith("_index") ])
                # in case, current files doesn't contains all language index files
                if current_index_files_set != self.section_index_files_set:
                    print "Initilize section: {0}".format(root)

                    set_to_add = self.section_index_files_set - (self.section_index_files_set & current_index_files_set)
                    set_to_remove = (self.section_index_files_set|current_index_files_set) - self.section_index_files_set

                    # create missing _index files
                    for f in set_to_add:
                        target_index_file = os.path.join(root, f)
                        try:
                            print(" - create file:{0}".format(target_index_file))
                            open(target_index_file, 'a').close()
                        except:
                            print "Failed to create {0} under {1}".format(f, root)
                            return False

                    # remove redundant
                    for f in set_to_remove:
                        target_index_file = os.path.join(root, f)
                        try:
                            print(" - remove file:{0}".format(target_index_file))
                            os.remove(target_index_file)
                        except:
                            print "Failed to remove {0} under {1}".format(f, root)
                            return False

    def get_lang_code(self, root, filename):
        absfile = os.path.join(root, filename)
        with io.open(absfile, "r", encoding='utf8') as f:
            file_content = f.read()

            if self.regex_contains_chinese_text.findall(file_content):
                return "zh"

        return "en"

    def rename_with_lang(self, root, filename):
        try:
            self.section_index_files_set
        except AttributeError:
            print("Rename pages with language setting doesnt' work")
            return False

        if filename in self.section_index_files_set:
            return ""

        # check if we need append lang suffix in filename or not
        with_lang_suffix = False
        default_lang_set = set([self.default_lang])
        config_lang_set = set(self.lang_list)
        if default_lang_set != config_lang_set:
            with_lang_suffix = True

        # remove all lang suffix
        if with_lang_suffix:
            self.add_lang_suffix(root, filename, config_lang_set)
        # add lang suffix
        else:
            self.remove_lang_suffix(root, filename)

    def remove_lang_suffix(self, root, filename):
        name_list = filename.split(".")
        part_num = len(name_list)

        # for files only have one ".", insert file_lang_code directly
        if part_num == 2:
            # no lang suffix found, skip it
            return ""
        elif part_num == 1:
            print "invalid filename"
            return ""
        elif part_num > 2:
            maybe_lang_code = name_list[-2]
            if maybe_lang_code not in self.lang_codes:
                # Skipped rename as it already contains langcode
                print("{0} is not a valid language code, skip it".format(maybe_lang_code))
                return ""
            else:
                first_part = ".".join(name_list[:-2])
                new_filename = "{0}.md".format(first_part)

        orig_file = os.path.join(root, filename)
        target_file = os.path.join(root, new_filename)

        try:
            print("Remove lang suffix for: {0} to: {1}".format(filename, new_filename))
            os.rename(orig_file, target_file)
        except:
            print "Failed to rename file from:{0} to {1}".format(filename, new_filename)
            traceback.print_exc()
            return ""

        return new_filename

    def add_lang_suffix(self, root, filename, config_lang_set):
        name_list = filename.split(".")
        part_num = len(name_list)

        file_lang_code = self.get_lang_code(root, filename)
        if file_lang_code not in config_lang_set:
            print("Cannot guess which lang suffix need append automatically!")
            return ""

        # for files only have one ".", insert file_lang_code directly
        if part_num == 2:
            new_filename = "{0}.{1}.md".format(name_list[0], file_lang_code)
        elif part_num == 1:
            print "invalid filename"
            return ""
        elif part_num > 2:
            maybe_lang_code = name_list[-2]
            if maybe_lang_code == file_lang_code:
                # Skipped rename as it already contains langcode
                return ""
            else:
                first_part =  ".".join(name_list[:-2])
                new_filename = "{0}.{1}.md".format(first_part, file_lang_code)

        orig_file = os.path.join(root, filename)
        target_file = os.path.join(root, new_filename)

        try:
            os.rename(orig_file, target_file)
        except:
            print "Failed to rename file from:{0} to:{1}".format(filename, new_filename)
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




