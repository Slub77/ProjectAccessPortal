
import os

from P4 import P4, P4Exception

import unittest

class p4_connection():
    def __enter__(self):
        p4 = P4()                        # Create the P4 instance
        self.p4 = p4
        p4.host = "localhost"
        p4.port = "1666"
        p4.user = "kalms"
        p4.connect()                   # Connect to the Perforce server
        return p4

    def __exit__(self, type, value, traceback):
        self.p4.disconnect()

class p4_workspace():

    def __init__(self, p4, workspace):
        self.p4 = p4
        self.workspace = workspace

    def __enter__(self):
        self.old_workspace = self.p4.client
        self.p4.client = self.workspace

    def __exit__(self, type, value, traceback):
        self.p4.client = self.old_workspace

def p4_get_users():
    with p4_connection() as p4:
        users = p4.run("users")
    return users

def p4_create_user(login, email, full_name):
    with p4_connection() as p4:
        p4.input = "User: " + login + "\n\n" + \
            "Email: " + email + "\n\n" + \
            "FullName: " + full_name + "\n\n"

        p4.run("user", "-i", "-f")

def p4_delete_user(login):
    with p4_connection() as p4:
        p4.run("user", "-d", "-f", login)

def p4_create_workspace(name, root, view):
    with p4_connection() as p4:
        view_as_strings = ""
        for view_depot_path, view_local_path in view:
            view_as_strings += "%s %s\n" % (view_depot_path, view_local_path)

        workspace = \
            'Client: ' + name + '\n\n' + \
            'Root: ' + root + '\n\n' + \
            'View: ' + view_as_strings + '\n\n'
        print workspace
        p4.save_client(workspace)

def p4_delete_workspace(name):
    with p4_connection() as p4:
        p4.run_client("-d", "-f", name)

def p4_add(workspace, local_file):
    with p4_connection() as p4:
        with p4_workspace(p4, workspace) as workspace_obj:
            p4.run_add(local_file)

def p4_submit(workspace, reason):
    with p4_connection() as p4:
        with p4_workspace(p4, workspace) as workspace_obj:
            p4.run_submit("-d", reason)

def p4_create_depot(name):
    with p4_connection() as p4:
        depot = \
            'Depot: ' + name + '\n\n' + \
            'Type: local' + '\n\n' + \
            'Map: ' + name + '/...' + '\n\n'
        p4.save_depot(depot)

def p4_delete_depot(name):
    with p4_connection() as p4:
        p4.run_depot("-d", "-f", name)


def p4_import_local_file(local_file, remote_path, reason):
    workspace_name = 'p4_import_local_file_workspace'
    view = [(remote_path, '//%s/%s' % (workspace_name, local_file))]
    p4_create_workspace(workspace_name, os.getcwd(), view)
    try:
        p4_add(workspace_name, local_file)
        p4_submit(workspace_name, reason)
        p4_delete_workspace(workspace_name)
    except:
        p4_delete_workspace(workspace_name)
        raise


class TestP4Methods(unittest.TestCase):

    DEPOT_NAME = 'unittest_test_depot'
    USER_NAME = 'unittest_test_user'
    WORKSPACE_NAME = 'unittest_test_workspace'

    def test_get_users(self):
        p4_get_users()

    def test_p4_create_and_delete_user(self):
        p4_create_user(self.USER_NAME, self.USER_NAME + "@example.com", "Unittest Test user")
        p4_delete_user(self.USER_NAME)

    def test_p4_create_and_delete_workspace(self):
        p4_create_depot(self.DEPOT_NAME)
        try:
            p4_create_workspace(self.WORKSPACE_NAME, '.', [('//%s/...' % self.DEPOT_NAME, '//%s/...' % self.WORKSPACE_NAME)])
            p4_delete_workspace(self.WORKSPACE_NAME)
        except:
            p4_delete_depot(self.DEPOT_NAME)
            raise

    def test_p4_create_file(self):
        p4_create_depot(self.DEPOT_NAME)
        try:
            p4_import_local_file('requirements.txt', '//%s/subdir/unittest.txt' % self.DEPOT_NAME, "Testing file import")
        except:
            p4_delete_depot(self.DEPOT_NAME)
            raise

if __name__ == '__main__':
    unittest.main()
