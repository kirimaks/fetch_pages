# -*- coding: utf-8 -*-
from pytagcloud import create_tag_image, create_html_data, make_tags, \
    LAYOUT_HORIZONTAL, LAYOUTS
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts
from string import Template
import os


my_text = "Kirill Kirill Washington_DC Apache_Foundation Apache_Foundation lets hope this works"

tags = make_tags(get_tag_counts(my_text), maxsize=120, colors=COLOR_SCHEMES['audacity'])
data = create_html_data(tags, (440,600), layout=LAYOUT_HORIZONTAL, fontname='PT Sans Regular')

template_file = open('html_template.html', 'r')
html_template = Template(template_file.read())

context = {}

tags_template = '<li class="cnt" style="top: %(top)dpx; left: %(left)dpx; height: %(height)dpx;"><a class="tag %(cls)s" href="#%(tag)s" style="top: %(top)dpx;\
        left: %(left)dpx; font-size: %(size)dpx; height: %(height)dpx; line-height:%(lh)dpx;">%(tag)s</a></li>'

context['tags'] = ''.join([tags_template % link for link in data['links']])
context['width'] = data['size'][0]
context['height'] = data['size'][1]
context['css'] = "".join("a.%(cname)s{color:%(normal)s;}\
        a.%(cname)s:hover{color:%(hover)s;}" %
                                  {'cname':k,
                                   'normal': v[0],
                                   'hover': v[1]}
                                 for k,v in data['css'].items())

html_text = html_template.substitute(context)

html_file = open('cloud.html', 'w')
html_file.write(html_text)
html_file.close()
