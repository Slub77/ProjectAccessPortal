
import os

from django.conf import settings

from P4 import P4, P4Exception

import unittest

import logging
logger = logging.getLogger(__name__)

class P4Connection(object):

    def __init__(self, host, port, user, password):
        self.p4 = P4()
        self.p4.host = host
        self.p4.port = port
        self.p4.user = user
        self.p4.password = password

    def __enter__(self):
        logger.debug("Connecting to P4")
        logger.debug(self.p4.connect())
        return self

    def __exit__(self, type, value, traceback):
        logger.debug("Disconnecting from P4")
        logger.debug(self.p4.disconnect())

    def connect(self):
        logger.debug("Connecting to P4")
        logger.debug(self.p4.connect())

    def disconnect(self):
        logger.debug("Disconnecting from P4")
        logger.debug(self.p4.disconnect())


    def get_users(self):
        logger.debug("Invoking P4 command: users")
        users = self.p4.run("users")
        logger.debug(users)
        return users

    def get_user(self, name):
        logger.debug("Invoking P4 command: users %s" % name)
        users = self.p4.run("users", name)
        logger.debug(users)
        return users

    def create_user(self, login, email, full_name):
        self.p4.input = \
            "User: " + login + "\n\n" + \
            "Email: " + email + "\n\n" + \
            "FullName: " + full_name + "\n\n"

        logger.debug("Invoking P4 command: user -i -f")
        logger.debug("Extra input: %s" % self.p4.input)
        logger.debug(self.p4.run("user", "-i", "-f"))

    def delete_user(self, login):
        logger.debug("Invoking P4 command: %s %s %s %s" % ("user", "-d", "-f", login))
        logger.debug(self.p4.run("user", "-d", "-f", login))

    def create_workspace(self, name, root, view):
        view_as_strings = ""
        for view_depot_path, view_local_path in view:
            view_as_strings += "%s %s\n" % (view_depot_path, view_local_path)

        workspace = \
            'Client: ' + name + '\n\n' + \
            'Root: ' + root + '\n\n' + \
            'View: ' + view_as_strings + '\n\n'
        logger.debug("Invoking P4 command: client -i")
        logger.debug("Extra input: %s" % workspace)
        logger.debug(self.p4.save_client(workspace))

    def delete_workspace(self, name):
        logger.debug("Invoking P4 command: client %s %s %s" % ("-d", "-f", name))
        logger.debug(self.p4.run_client("-d", "-f", name))

    def add(self, workspace, local_file):
        with p4_workspace(self.p4, workspace) as workspace_obj:
            logger.debug("Invoking P4 command: add %s" % local_file)
            logger.debug(self.p4.run_add(local_file))

    def submit(self, workspace, reason):
        with p4_workspace(self.p4, workspace) as workspace_obj:
            logger.debug("Invoking P4 command: submit %s %s" % ("-d", reason))
            logger.debug(self.p4.run_submit("-d", reason))

    def create_depot(self, name):
        depot = \
            'Depot: ' + name + '\n\n' + \
            'Type: local' + '\n\n' + \
            'Map: ' + name + '/...' + '\n\n'
        logger.debug("Invoking P4 command: depot -i")
        logger.debug("Extra input: %s" % depot)
        logger.debug(self.p4.save_depot(depot))

    def delete_depot(self, name):
        logger.debug("Invoking P4 command: depot %s %s %s" % ("-d", "-f", name))
        self.p4.run_depot("-d", "-f", name)

    def obliterate_file(self, file):
        logger.debug("Invoking P4 command: obliterate %s %s" % ("-y", file))
        logger.debug(self.p4.run_obliterate("-y", file))

    def file_exists(self, file):
        try:
            logger.debug("Invoking P4 command: files %s %s %s %s" % ("-e", "-m", "1", file))
            result = self.p4.run_files("-e", "-m", "1", file)
            logger.debug(result)
            return True
        except:
            return False

    def import_local_file(self, local_file, remote_path, reason):
        workspace_name = 'p4_import_local_file_workspace'
        view = [(str(remote_path), str('//%s/%s' % (workspace_name, local_file)))]
        self.create_workspace(workspace_name, os.getcwd(), view)
        try:
            self.add(workspace_name, str(local_file))
            self.submit(workspace_name, reason)
            self.delete_workspace(workspace_name)
        except:
            self.delete_workspace(workspace_name)
            raise

    def read_protect(self):
        logger.debug("Invoking P4 command: protect -o")
        protections = self.p4.run_protect('-o')
        logger.debug(protections)
        return protections[0]['Protections']

    def write_protect(self, protections):
        logger.debug("Invoking P4 command: protect -i")
        logger.debug("Extra input: %s" % [{'Protections': protections}])
        logger.debug(self.p4.save_protect([{'Protections': protections}]))

    def get_groups(self):
        logger.debug("Invoking P4 command: groups")
        groups = self.p4.run_groups()
        logger.debug(groups)
        return groups

    def read_group_members(self, name):
        logger.debug("Invoking P4 command: group %s %s" % ("-o", name))
        group = self.p4.run_group("-o", name)
        logger.debug(group)

        if 'Users' in group[0]:
            users = group[0]['Users']
        else:
            users = []

        if 'Subgroups' in group[0]:
            subgroups = group[0]['Subgroups']
        else:
            subgroups = []

        return (users, subgroups)

    def write_group_members(self, name, users, subgroups):
        logger.debug("Invoking P4 command: group %s %s" % ("-o", name))
        group = self.p4.run_group("-o", name)
        logger.debug(group)
        group[0]['Users'] = users
        group[0]['Subgroups'] = subgroups
        logger.debug("Invoking P4 command: group -i")
        logger.debug("Extra input: %s" % group)
        logger.debug(self.p4.save_group(group))

    def delete_group(self, name):
        logger.debug("Invoking P4 command: group %s %s" % ("-d", name))
        logger.debug(self.p4.run_group("-d", name))

    def add_user_to_group(self, group, user):
        (users, subgroups) = self.read_group_members(group)
        if not user in users:
            self.write_group_members(group, users + [user], subgroups)

    def remove_user_from_group(self, group, user):
        (users, subgroups) = self.read_group_members(group)
        if user in users:
            users.remove(user)
            self.write_group_members(group, users, subgroups)

    def add_subgroup_to_group(self, group, subgroup):
        (users, subgroups) = self.read_group_members(group)
        if not subgroup in subgroups:
            self.write_group_members(group, users, subgroups + [subgroup])

    def remove_subgroup_from_group(self, group, subgroup):
        (users, subgroups) = self.read_group_members(group)
        if subgroup in subgroups:
            subgroups.remove(subgroup)
            self.write_group_members(group, users, subgroups)

class p4_workspace():

    def __init__(self, p4, workspace):
        self.p4 = p4
        self.workspace = workspace

    def __enter__(self):
        self.old_workspace = self.p4.client
        logger.debug("Changing active P4 workspace to %s" % self.workspace)
        self.p4.client = self.workspace

    def __exit__(self, type, value, traceback):
        logger.debug("Changing active P4 workspace to %s" % self.old_workspace)
        self.p4.client = self.old_workspace


class P4ConnectionAsServiceUser(P4Connection):

    def __init__(self):
        super(P4ConnectionAsServiceUser, self).__init__(settings.PERFORCE['HOST'], settings.PERFORCE['PORT'], settings.PERFORCE['SERVICE_USER'], settings.PERFORCE['SERVICE_PASSWORD'])


class TestP4Methods(unittest.TestCase):

    P4HOST = 'localhost'
    P4PORT = '1666'
    P4USER = 'kalms.m'
    P4PASSWORD = 'kalms.m'

    DEPOT_NAME = 'unittest_test_depot'
    USER_NAME = 'unittest_test_user'
    WORKSPACE_NAME = 'unittest_test_workspace'
    GROUP_NAME = 'unittest_test_group'
    SUBGROUP_NAME = 'unittest_test_subgroup'

    USER_EMAIL = USER_NAME + '@example.com'
    USER_FULL_NAME = 'Unittest Test User'

    def test_get_users(self):
        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER, self.P4PASSWORD) as p4:
            p4.get_users()

    def test_p4_create_and_delete_user(self):
        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER, self.P4PASSWORD) as p4:
            p4.create_user(self.USER_NAME, self.USER_EMAIL, self.USER_FULL_NAME)
            p4.delete_user(self.USER_NAME)

    def test_p4_create_and_delete_workspace(self):
        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER, self.P4PASSWORD) as p4:
            p4.create_depot(self.DEPOT_NAME)
            try:
                p4.create_workspace(self.WORKSPACE_NAME, '.', [('//%s/...' % self.DEPOT_NAME, '//%s/...' % self.WORKSPACE_NAME)])
                p4.delete_workspace(self.WORKSPACE_NAME)
            except:
                p4.delete_depot(self.DEPOT_NAME)
                raise

    def test_p4_create_file(self):
        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER, self.P4PASSWORD) as p4:
            p4.create_depot(self.DEPOT_NAME)
            try:
                p4.import_local_file('requirements.txt', '//%s/subdir/unittest.txt' % self.DEPOT_NAME, "Testing file import")
                p4.obliterate_file('//%s/subdir/unittest.txt' % self.DEPOT_NAME)
                p4.delete_depot(self.DEPOT_NAME)
            except:
                p4.delete_depot(self.DEPOT_NAME)
                raise

    def test_p4_protect(self):
        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER, self.P4PASSWORD) as p4:

            protect_line = "write user %s * //..." % self.USER_NAME

            protections = p4.read_protect()

            protections2 = protections + [protect_line]
            p4.write_protect(protections2)

            protections3 = p4.read_protect()
            self.assertIn(protect_line, protections3)

            p4.write_protect(protections)

            protections4 = p4.read_protect()
            self.assertNotIn(protect_line, protections4)

    def test_p4_groups_1(self):

        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER, self.P4PASSWORD) as p4:

            p4.create_user(self.USER_NAME, self.USER_EMAIL, self.USER_FULL_NAME)
            try:
                try:
                    self.assertFalse(p4.read_group_members(self.GROUP_NAME)[0])
                    self.assertFalse(p4.read_group_members(self.GROUP_NAME)[1])

                    p4.write_group_members(self.GROUP_NAME, [self.USER_NAME], [])
                    self.assertIn(self.USER_NAME, p4.read_group_members(self.GROUP_NAME)[0])
                    self.assertFalse(p4.read_group_members(self.GROUP_NAME)[1])

                    p4.write_group_members(self.GROUP_NAME, [], [])
                    self.assertFalse(p4.read_group_members(self.GROUP_NAME)[0])
                    self.assertFalse(p4.read_group_members(self.GROUP_NAME)[1])

                    p4.write_group_members(self.GROUP_NAME, [self.USER_NAME], [])
                    self.assertIn(self.USER_NAME, p4.read_group_members(self.GROUP_NAME)[0])
                    self.assertFalse(p4.read_group_members(self.GROUP_NAME)[1])

                    p4.delete_group(self.GROUP_NAME)
                    self.assertFalse(p4.read_group_members(self.GROUP_NAME)[0])
                    self.assertFalse(p4.read_group_members(self.GROUP_NAME)[1])
                except:
                    p4.delete_group(self.GROUP_NAME)
                    raise

                p4.delete_user(self.USER_NAME)
            except:
                p4.delete_user(self.USER_NAME)
                raise

    def test_p4_groups_2(self):

        with P4Connection(self.P4HOST, self.P4PORT, self.P4USER, self.P4PASSWORD) as p4:

            p4.create_user(self.USER_NAME, self.USER_EMAIL, self.USER_FULL_NAME)
            try:
                self.assertFalse(p4.read_group_members(self.GROUP_NAME)[0])
                self.assertFalse(p4.read_group_members(self.GROUP_NAME)[1])
                self.assertFalse(p4.read_group_members(self.SUBGROUP_NAME)[0])
                self.assertFalse(p4.read_group_members(self.SUBGROUP_NAME)[1])

                p4.add_user_to_group(self.SUBGROUP_NAME, self.USER_NAME)
                self.assertIn(self.USER_NAME, p4.read_group_members(self.SUBGROUP_NAME)[0])

                p4.add_user_to_group(self.GROUP_NAME, self.USER_NAME)
                self.assertIn(self.USER_NAME, p4.read_group_members(self.GROUP_NAME)[0])

                self.assertIn(self.USER_NAME, p4.read_group_members(self.GROUP_NAME)[0])
                self.assertFalse(p4.read_group_members(self.GROUP_NAME)[1])

                p4.add_subgroup_to_group(self.GROUP_NAME, self.SUBGROUP_NAME)
                self.assertIn(self.USER_NAME, p4.read_group_members(self.GROUP_NAME)[0])
                self.assertIn(self.SUBGROUP_NAME, p4.read_group_members(self.GROUP_NAME)[1])

                p4.remove_user_from_group(self.GROUP_NAME, self.USER_NAME)
                self.assertNotIn(self.USER_NAME, p4.read_group_members(self.GROUP_NAME)[0])

                p4.remove_subgroup_from_group(self.GROUP_NAME, self.SUBGROUP_NAME)
                self.assertNotIn(self.SUBGROUP_NAME, p4.read_group_members(self.GROUP_NAME)[1])

                p4.remove_user_from_group(self.SUBGROUP_NAME, self.USER_NAME)
                self.assertNotIn(self.USER_NAME, p4.read_group_members(self.SUBGROUP_NAME)[0])

                p4.delete_user(self.USER_NAME)
            except:
                try:
                    p4.delete_group(self.GROUP_NAME)
                except:
                    pass

                try:
                    p4.delete_group(self.SUBGROUP_NAME)
                except:
                    pass

                try:
                    p4.delete_user(self.USER_NAME)
                except:
                    pass

                raise

if __name__ == '__main__':
    unittest.main()
