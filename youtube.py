from markdown.extensions import Extension
from markdown.inlinepatterns import LinkInlineProcessor
import urllib.parse
import xml.etree.ElementTree as etree
import os
import re

import logging

# ![alttxt](http://x.com/) or ![alttxt](<http://x.com/>)
IMAGE_LINK_RE = r'\!\['

def tToStart(tstr):
    # 2m30s -> 60*2 + 30
    try:
        if tstr.isnumeric():
            return tstr
    except:
        logging.warning(f"Got non-string t= param {tstr!r}", exc_info=True)
    try:
        match = re.search(r"^(?:(?P<h>\d+)h){0,1}(?:(?P<m>\d+)m){0,1}(?:(?P<s>\d+)s){0,1}$", tstr)
        groupdict = match.groupdict()
        return int(groupdict["s"] or 0) + 60 * (int(groupdict["m"] or 0) + 60 * (int(groupdict["h"] or 0)))
    except:
        logging.warning(f"Improperly formatted youtube t= param {tstr!r}", exc_info=True)
        return tstr

assert tToStart("1m30s") == 90
assert tToStart("1h30s") == 3630
assert tToStart("350s") == 350

class YoutubeVideoInlineProcessor(LinkInlineProcessor):
    """ Return a img element from the given match. """

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        href, video_id, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        parsed_query = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)

        if "v" in parsed_query:
            parsed_query.pop("v")
        if "t" in parsed_query:
            parsed_query["start"] = tToStart(parsed_query["t"][0])
            parsed_query.pop("t")
        parsed_query["autoplay"] = "1"

        out_query = urllib.parse.urlencode(parsed_query, doseq=True)

        el = etree.Element("div")
        el.set("class", "lazyframe")
        el.set("data-vendor", "youtube")
        el.set("style", f"background-image: url(https://img.youtube.com/vi/{video_id}/hqdefault.jpg);")

        el.set("onclick", f'this.outerHTML = `<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/{video_id}?{out_query}" title="{self.unescape(text)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture" allowfullscreen class="media"></iframe>`')

        # sub_title = etree.SubElement(el, "span")
        # sub_title.set("class", "lazyframe__title")
        # sub_title.text = repr(title)
        # for k, v in {
        #     "src": f"https://www.youtube-nocookie.com/embed/{video_id_params}",
        #     "frameborder": "0",
        #     "allow": "accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture",
        #     "allowfullscreen": "1",
        #     "width": "560",
        #     "height": "315", 
        #     "alt": self.unescape(text)
        # }.items():
        #     el.set(k, v)

        return el, m.start(0), index

    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        if handled:
            match = re.search(r"((youtube.com\/watch\?v=)|(youtu.be\/)|(youtube.com\/embed\/))([A-Za-z0-9-_]+)(\?|&|$)", href)
            if match:
                return href, match.group(5), title, index, handled
        return None, None, None, None, None


class YoutubeVideoExtension(Extension):

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            YoutubeVideoInlineProcessor(IMAGE_LINK_RE, md),
            'youtube_video_link', 180
        )


def makeExtension(**kwargs):
    return YoutubeVideoExtension(**kwargs)
