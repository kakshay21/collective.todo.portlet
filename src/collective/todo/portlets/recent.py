# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from collective.todo import _
from plone import schema
from plone.app.portlets.portlets import base
from z3c.form import field
from zope.interface import implements
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import json
import urllib
import urllib2


class IRecentPortlet(IPortletDataProvider):
    place_str = schema.TextLine(title=_(u'Name of your place with country code'),
                       description=_(u'City name along with country code i.e Delhi,IN'),
                       required=True,
                       default=u'delhi,in')


class Assignment(base.Assignment):
    implements(IRecentPortlet)
    schema = IRecentPortlet

    def __init__(self,place_str='delhi,in'):
        self.place_str = place_str.lower()

    @property
    def title(self):
        return _(u"Place weather")


class AddForm(base.AddForm):
    schema = IRecentPortlet
    form_fields = field.Fields(IRecentPortlet)
    label = _(u"Add Place weather")
    description = _(u"This portlet displays weather of the place.")

    def create(self, data):
        return Assignment(
            place_str=data.get('place_str', 'delhi,in'),
        )


class EditForm(base.EditForm):
    schema = IRecentPortlet
    form_fields = field.Fields(IRecentPortlet)
    label = _(u"Edit Place weather")
    description = _(u"This portlet displays weather of the place.")


class Renderer(base.Renderer):
    schema = IRecentPortlet
    _template = ViewPageTemplateFile('recent.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()

    def render(self):
        return self._template()   

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        return not self.anonymous and len(self._data())

    def weather_report(self):
        self.result = self._data()
        return self.result['description']

    def get_humidity(self):
        return self.result['humidity']
    
    def get_pressure(self):
        return self.result['pressure']

    @memoize
    def _data(self):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="{}")'.format(
            self.data.place_str,
        )
        yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)
        result = {}
        result['description'] = data['query']['results']['channel']['description']
        result['pressure'] = data['query']['results']['channel']['atmosphere']['pressure']
        result['humidity'] = data['query']['results']['channel']['atmosphere']['humidity']
        return result
