
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


class TestP4Methods(unittest.TestCase):

    def test_get_users(self):
        print p4_get_users()

    def test_p4_create_and_delete_user(self):
        p4_create_user("unittest_test_user", "unittest_test_user@example.com", "Unittest Test user")
        p4_delete_user("unittest_test_user")

if __name__ == '__main__':
    unittest.main()
