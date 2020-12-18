# Gio's Markdown Plugins

they're all single-files because come *on*

## html5video

Native HTML5 video tags using the same syntax as inline image embeds.

### Usage

Just embed video files as if they were images. Video files are detected based on their file extension.

```markdown
![alt](./video.mp4)
```


## Spoiler box

Markdown only.

Implements bbcode-style spoiler boxes, which can be used to collapse and expand sections of content.

### Usage

Use the tag surrounding standard markdown.

```markdown
[spoiler]
This is *true* markdown text.

Markdown allows you to be lazy and only put the `>` before the first
line of a hard-wrapped paragraph:

> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
[spoiler]
```

There is an alternate syntax wherein `[spoiler]` takes a "parameter", which is used to style the spoiler box button.

```markdown
[spoiler Content]
Some big images
[spoiler]
```

This will show as "Show Content" and "Hide Content" instead of "Show Spoiler".

Spoiler boxes can be nested arbitrarily.

Spoiler contents are considered an inline part of the parent document, and can contain elements like `[TOC]`. The spoiler box is added at the very end of processing.

Suggested CSS would be something like:

```css
/* Spoiler tags */
button.spoiler-button {
    margin-left: auto;
    margin-right: auto;
    display: block;
}

.spoiler-wrapper {
    border: dashed gray 1px;
    margin: 32px 0px;
    padding: 1px 35px;
}
```

Note: Including headers inside spoiler boxes is *not* recommended for various semantic reasons, including

- Inconsistent anchorlink behaviour
- Incompatibility with plugins like [outline](https://github.com/aleray/mdx_outline)
