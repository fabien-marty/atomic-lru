import os
import re


def define_env(env):
    @env.macro
    def include_markdown(filename: str, increment: int = 0) -> str:
        docs_dir = env.conf.get("docs_dir", "docs")
        full_filename = os.path.join(env.project_dir, docs_dir, filename)
        with open(full_filename) as f:
            lines = f.readlines()
        new_lines: list[str] = []
        for line in lines:
            if re.match(r"^#+ ", line):
                new_lines.append("#" * increment + line)
            else:
                new_lines.append(line)
        return env.render("".join(new_lines))


def on_post_page_macros(env):
    if env.page.title == "Atomic LRU":
        with open("README.md", "w") as f:
            f.write("<!-- *** GENERATED FILE - DO NOT EDIT *** -->\n")
            f.write(env.markdown)
