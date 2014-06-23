# -*- coding: utf-8 -*-
"""
Site tools feeds module
===============================================

.. module:: sitetools.feeds
    :platform: Django
    :synopsis: Site tools feeds module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

class BaseRSSFeedGenerator(Rss201rev2Feed):
    """
    Enhanced base feed generator class to add several features
    """
    # Set feed mime type to application/xml
    mime_type = 'application/xml'

    def add_root_elements(self, handler):
        # Call parent class method
        super(BaseRSSFeedGenerator, self).add_root_elements(handler)

        feed=self.feed

        # Feed hub
        if 'hub_url' in feed and feed['hub_url'] is not None:
            handler.addQuickElement('link', '', {
                'rel': 'hub',
                'href': feed['hub_url'],
                'xmlns': 'http://www.w3.org/2005/Atom'
            })
        
        # Feed image
        if 'image_url' in feed and feed['image_url'] is not None:
            handler.startElement('image',{})
            handler.addQuickElement('url', feed['image_url'])
            handler.addQuickElement('title', feed['title'])
            handler.addQuickElement('link', feed['link'])
            handler.endElement(u'image')

class BaseRSSFeed(Feed):
    """
    Enhanced base feed class
    """
    feed_type=BaseRSSFeedGenerator

    def feed_extra_kwargs(self,obj):
        return {
            'hub_url': getattr(self, 'hub_url', None),
            'image_url': getattr(self, 'image_url', None)
        }