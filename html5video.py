from markdown.extensions import Extension
from markdown.inlinepatterns import LinkInlineProcessor
import urllib.parse
import xml.etree.ElementTree as etree
import os


# ![alttxt](http://x.com/) or ![alttxt](<http://x.com/>)
IMAGE_LINK_RE = r'\!\['

# MP4 video/mp4
# WebM    video/webm
# Ogg video/ogg


VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg"}


class VideoInlineProcessor(LinkInlineProcessor):
    """ Return a img element from the given match. """

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, mtype, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = etree.Element("video")

        src_query = urllib.parse.urlparse(src).query
        src_query_dict = urllib.parse.parse_qs(src_query)

        el.set("src", src)
        el.set("type", mtype)

        if title is not None:
            el.set("title", title)

        if src_query_dict.get("gifmode"):
            for param in ["nocontrols", "autoplay", "muted"]:
                src_query_dict[param] = ["1"]

        if not src_query_dict.get("nocontrols"):
            el.set("controls", "true")

        for opt_prop in ["autoplay", "muted"]:
            if src_query_dict.get(opt_prop) is not None:
                el.set(opt_prop, "true")

        el.set('alt', self.unescape(text))
        return el, m.start(0), index

    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        if handled:
            linkext = os.path.splitext(urllib.parse.urlparse(href).path)[1].lower()
            if linkext in VIDEO_EXTENSIONS:
                mtype = f"video/{linkext.replace('.', '')}"
                return href, title, index, mtype, handled
        return None, None, None, None, None


class VideoExtension(Extension):

    def extendMarkdown(self, md):
        md.inlinePatterns.register(VideoInlineProcessor(IMAGE_LINK_RE, md), 'video_link', 180)


def makeExtension(**kwargs):
    return VideoExtension(**kwargs)
