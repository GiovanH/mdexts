from markdown.extensions import Extension
from markdown.inlinepatterns import LinkInlineProcessor
import urllib.parse
import xml.etree.ElementTree as etree
import os
import re


# ![alttxt](http://x.com/) or ![alttxt](<http://x.com/>)
IMAGE_LINK_RE = r'\!\['



class YoutubeVideoInlineProcessor(LinkInlineProcessor):
    """ Return a img element from the given match. """

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        video_id_params, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        video_id_params = "DdA_axFJZSg?start=8"

        el = etree.Element("iframe")

        for k, v in {
            "src": f"https://www.youtube-nocookie.com/embed/{video_id_params}",
            "frameborder": "0",
            "allow": "accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture",
            "allowfullscreen": "1",
            "width": "560",
            "height": "315", 
            "alt": self.unescape(text)
        }.items():
            el.set(k, v)

        return el, m.start(0), index

    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        if handled:
            match = re.search(r"((youtube.com\/watch\?v=)|(youtu.be\/))(.+)$", href)
            if match:
                return match.group(3), title, index, handled
        return None, None, None, None


class YoutubeVideoExtension(Extension):

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            YoutubeVideoInlineProcessor(IMAGE_LINK_RE, md),
            'youtube_video_link', 180
        )


def makeExtension(**kwargs):
    return YoutubeVideoExtension(**kwargs)
