# -*- coding: utf-8 -*-
import markdown
from jinja2 import Template
import re
import logging


MATCH_RE = r"(\[spoiler( .+?){0,1}\])([\S\s]*?)(\[\/spoiler\])"

SCRIPT_PREREQ = """
<script>
    function loggle(button, hidetext, showtext) {
        table = button.parentNode.children[1];
        if (table.style.display == 'none') {
            // We were hidden, now show.
            table.style.display = 'block';
            button.innerText = hidetext;
        } else {
            table.style.display = 'none';
            button.innerText = showtext;
        }
        return false;
    }
</script>
"""

TEMPLATE_PRE = Template("""<div class="spoiler-wrapper">
    <button type="button" class="spoiler-button" onclick="loggle(this, 'Hide {{ desc }}', 'Show {{ desc }}')">
        Show {{ desc }}
    </button>
    <div class="spoiler-content" markdown="1" style="display: none">
""")
        
TEMPLATE_POST = Template("""    </div>
</div>""")

class SpoilerMdExtension(markdown.Extension):

    def extendMarkdown(self, md):
        """ Add SpoilerblockPreprocessor to the Markdown instance. """
        # md.registerExtension(self)
        md.preprocessors.register(SpoilerblockPreprocessor(md), 'spoiler_block', 29)  # Must be < 30


class SpoilerblockPreprocessor(markdown.preprocessors.Preprocessor):
    def run(self, lines):
        RE = re.compile(MATCH_RE, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        text = "\n".join(lines)
        inserted_script = False

        while True:
            match = RE.search(text)
            if match:

                before = text[:match.start()]
                after = text[match.end():]

                pretag, desc, content, posttag = match.groups()
                desc = desc[1:] if desc else "Spoiler"
                
                # logging.debug("Found spoiler wrapped content")
                # logging.debug(content)

                pre_html = TEMPLATE_PRE.render(desc=desc, content=content)
                post_html = TEMPLATE_POST.render(desc=desc, content=content)
                if not inserted_script:
                    # logging.info("Inserting script for first spoilerbox")
                    pre_html = SCRIPT_PREREQ + pre_html
                    inserted_script = True

                # These HTML blocks get shelved so that the inner content gets rendered as usual.

                # Ok so this is actually the dumbest hack ever to work around a hideous bug
                # The markdown processor usually doesn't process text inside HTML.
                # The whole point of stashing the HTML part is to let the markdown processor
                # process the file as if it were flat even though it's actually nested HTML.
                # But the stash tag *itself* *does* get processed as text and wrapped in paragraph tags,
                # so we have to perform an HTML injection attack on ourself here to unescape our content.
                pre_html = self.md.htmlStash.store("</p>" + pre_html + "<p>")
                post_html = self.md.htmlStash.store("</p>" + post_html + "<p>")

                text = "\n".join([before, pre_html, content, post_html, after])
            else:
                break
        return text.split("\n")


def makeExtension(**kwargs):
    return SpoilerMdExtension(**kwargs)
