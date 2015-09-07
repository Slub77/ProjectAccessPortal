
from P4Connection import P4Connection
from models import PAUser, PAProject, PAUserProjectAccess

from django.test import TestCase
import unittest

from project_actions import create_new_project, delete_project, add_user_to_project, remove_user_from_project

class TestProjectManagementMethods(TestCase):

    P4HOST = 'localhost'
    P4PORT = '1666'
    P4USER = 'kalms'

    DEPOT_NAME = 'unittest_test_depot'
    USER_NAME = 'unittest_test_user'
    WORKSPACE_NAME = 'unittest_test_workspace'
    GROUP_NAME = 'unittest_test_group'
    SUBGROUP_NAME = 'unittest_test_subgroup'

    USER_EMAIL = USER_NAME + '@example.com'
    USER_FULL_NAME = 'Unittest Test User'

    PROJECT_NAME = 'unittest_test_project'

    def setUp(self):

        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER) as p4:
            p4.create_depot(self.DEPOT_NAME)
            self.user = PAUser.objects.create(name=self.USER_NAME)
            p4.create_user(self.USER_NAME, self.USER_EMAIL, self.USER_FULL_NAME)

    def test_project_creation_and_removal(self):

        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER) as p4:
            project = None
            try:
                project = create_new_project(self.PROJECT_NAME)
                delete_project(project)
                project = None
            except:
                if project:
                    delete_project(project)
                raise

    def test_add_and_remove_user(self):

        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER) as p4:
            project = None
            project_access = None
            try:
                project = create_new_project(self.PROJECT_NAME)
                project_access = add_user_to_project(project, self.user)
                remove_user_from_project(project_access)
            except:
                if project_access:
                    remove_user_from_project(project_access)
                if project:
                    delete_project(project)
                raise

    def tearDown(self):

        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER) as p4:
            p4.delete_depot(self.DEPOT_NAME)
            p4.delete_user(self.USER_NAME)
