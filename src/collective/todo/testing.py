# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.todo


class CollectiveTodoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.todo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.todo:default')


COLLECTIVE_TODO_FIXTURE = CollectiveTodoLayer()


COLLECTIVE_TODO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_TODO_FIXTURE,),
    name='CollectiveTodoLayer:IntegrationTesting',
)


COLLECTIVE_TODO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TODO_FIXTURE,),
    name='CollectiveTodoLayer:FunctionalTesting',
)


COLLECTIVE_TODO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_TODO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveTodoLayer:AcceptanceTesting',
)
