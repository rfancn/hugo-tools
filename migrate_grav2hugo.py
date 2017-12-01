import os
import shutil
import frontmatter
import json
import datetime

def get_files_count(dir_path):
  files = []
  for f in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, f)):
       files.append(f)

  return len(files)      

def local_copy(root_dir, orig_filename):
  orig_file = os.path.join(root_dir, orig_filename)
  target_file = os.path.join(root_dir, "index.md")
  
  print "copy %s %s" % (orig_file, target_file)
  shutil.copy2(orig_file, target_file)
  os.remove(orig_file)
  return target_file

def move_to_parent(root_dir, orig_filename):
  target_dirname = os.path.dirname(root_dir)
  target_filename = os.path.basename(root_dir)
  orig_file = os.path.join(root_dir, orig_filename)
  target_file = os.path.join(target_dirname, target_filename + ".md")

  print "copy %s %s" % (orig_file, target_file)
  shutil.copy2(orig_file, target_file)

  os.remove(orig_file)
  os.rmdir(root_dir)

  return target_file
 
def process(f):
  stat = os.stat(f)
  post = frontmatter.load(f)

  # change time
  date = post.get("date")
  if not date:
    post["date"] = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

  lastmod = post.get("lastmod")
  if not lastmod:
    post["lastmod"] = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
  
  # change routes to alias
  routes = post.get("routes", None)
  if routes:
    al = []
    al.append(routes["default"])

    post["aliases"] = al 
    del post["routes"]

  # taxonomy:
  # category:
  # - blog
  # tag:
  # - TAG.BLOG.TUTORIAL
  taxonomy = post.get("taxonomy", None)
  if taxonomy:
    t = taxonomy.get("tag", None)
    if t:
      post["tags"] = t 

    c = taxonomy.get("category", None)
    if c:
      post["categories"] = c 

    del post["taxonomy"] 

  frontmatter.dump(post, f,  allow_unicode=True)

  os.utime(f, (stat.st_mtime, stat.st_mtime))

for root, dirs, files in os.walk("./content"):
    for f in files:
      if f == "post.md":
        # check how many files in root
        sibling_num = get_files_count(root)
        if sibling_num > 1:
          print "keep dir"
          newf = local_copy(root, f)
        else:
          newf = move_to_parent(root, f)

        process(newf)
        
        
      
        
