# hugo-tools
a collection of tools to maintain Hugo site

# How to use it
- git clone the repository to your hugo site root
    
    $ cd <hugo_site_root>
    $ git clone https://github.com/rfancn/hugo-tools.git
    $ python hugo-tools/<command>.py [options]
    
# Publish pages
Publish pages under content dir, it will do following:

- Automatically rename the page files to language sensitive one
- Maintain specific frontmatter attributes
- Make sure "_index.[language].md" files created for each directory except "content dir"
- If "draft=true" is defined in page files, then it will be skipped

- <content_dir>: required, content_dir is the hugo site content dir
- <exclude_regex>: optional, regular expression to filter out the pages by filename comparision

    $ cd <hugo_site_root>
    $ python hugo-tools/remove_taxonomy.py <content_dir> <exclude_regex>
    
e,g: All pages with filename "invisible*" will not publish

    $ cd <hugo_site_root>
    $ python hugo-tools/remove_taxonomy.py ./content "invisible*"


# Remove taxonomy
Remove specified taxonomy from all pagge under content dir

- <content_dir>: content_dir is the hugo site content dir
- <taxonomy string>: a string separated taxonomy by ",", e,g: "tags,categories"

    $ cd <hugo_site_root>
    $ python hugo-tools/remove_taxonomy.py <content_dir> <taxonomy string>
    
e,g:

    $ cd <hugo_site_root>
    $ python hugo-tools/remove_taxonomy.py ./content "categories"
    
