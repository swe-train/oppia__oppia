# coding: utf-8
#
# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the GAE current user services."""

from __future__ import absolute_import  # pylint: disable=import-only-modules
from __future__ import unicode_literals  # pylint: disable=import-only-modules

from core.platform.users import gae_current_user_services
from core.tests import test_utils

from google.appengine.api import users


class GaeCurrentUserServicesTests(test_utils.GenericTestBase):

    # User id of owner email generated by GAE.
    EXPECTED_OWNER_USER_ID = '176177241684014293971'

    def test_create_login_url(self):
        login_url = gae_current_user_services.create_login_url('')
        self.assertEqual(
            login_url,
            'https://www.google.com/accounts/Login' +
            '?continue=http%3A//localhost/signup%3Freturn_url%3D')

    def test_get_current_user(self):
        self.login(self.OWNER_EMAIL)
        current_user = gae_current_user_services.get_current_user()
        self.assertEqual(
            current_user,
            users.User(
                email=self.OWNER_EMAIL,
                _user_id=self.EXPECTED_OWNER_USER_ID
            )
        )
        self.logout()

        current_user = gae_current_user_services.get_current_user()
        self.assertEqual(current_user, None)

    def test_is_current_user_super_admin(self):
        self.login(self.OWNER_EMAIL)
        is_super_admin = gae_current_user_services.is_current_user_super_admin()
        self.assertEqual(is_super_admin, False)
        self.logout()

        self.login(self.ADMIN_EMAIL, is_super_admin=True)
        is_super_admin = gae_current_user_services.is_current_user_super_admin()
        self.assertEqual(is_super_admin, True)
        self.logout()

        is_super_admin = gae_current_user_services.is_current_user_super_admin()
        self.assertEqual(is_super_admin, False)

    def test_get_user_id_from_email(self):
        # Existing user scenario.
        user_id = gae_current_user_services.get_gae_id_from_email(
            self.OWNER_EMAIL)
        self.assertEqual(user_id, self.EXPECTED_OWNER_USER_ID)

        # Non-existing user scenario.
        user_id = gae_current_user_services.get_gae_id_from_email('')
        self.assertEqual(user_id, None)

    def test_get_current_gae_id(self):
        self.login(self.OWNER_EMAIL)
        user_id = gae_current_user_services.get_current_gae_id()
        self.assertEqual(user_id, self.EXPECTED_OWNER_USER_ID)
        self.logout()

        user_id = gae_current_user_services.get_current_gae_id()
        self.assertEqual(user_id, None)

    def test_get_current_user_email(self):
        self.login(self.OWNER_EMAIL)
        email = gae_current_user_services.get_current_user_email()
        self.assertEqual(email, self.OWNER_EMAIL)
        self.logout()

        email = gae_current_user_services.get_current_user_email()
        self.assertEqual(email, None)