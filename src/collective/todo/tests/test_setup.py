# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.todo.testing import COLLECTIVE_TODO_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.todo is properly installed."""

    layer = COLLECTIVE_TODO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.todo is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.todo'))

    def test_browserlayer(self):
        """Test that ICollectiveTodoLayer is registered."""
        from collective.todo.interfaces import (
            ICollectiveTodoLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveTodoLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_TODO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.todo'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.todo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.todo'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveTodoLayer is removed."""
        from collective.todo.interfaces import \
            ICollectiveTodoLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveTodoLayer,
            utils.registered_layers())
