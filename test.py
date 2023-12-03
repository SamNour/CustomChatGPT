import os
import shutil
import re

for dir in os.listdir("./promptflow"):
    if "jinja2" not in dir:
        continue
    m = re.search(r"([^\./\\]+)\.jinja2", dir)
    print(dir)
    # print(m.group(1))
    shutil.copy(os.path.join("./promptflow", dir), os.path.join("./prompts", m.group(1) + ".txt"))