
from p4access import P4Connection

import os

import logging
logger = logging.getLogger(__name__)

def create_default_project_user():

    with P4Connection('localhost', '1666', 'kalms') as p4:
            p4.create_user('default_project_user', 'no_email', 'default project user')

def create_missing_p4_users():

    with P4Connection('localhost', '1666', 'kalms') as p4:

        from models import MetaUser
        for meta_user in MetaUser.objects.all():
            if meta_user.ldap_user:
                if not meta_user.p4_user:
                    setup_student_in_p4(p4, meta_user.ldap_user.uid, meta_user.ldap_user.mail, meta_user.ldap_user.cn)

def generate_protect_lines_for_user(name):
    protect_lines = [
            str('write user %s * //Users/%s/Private/...' % (name, name)),
            str('write user %s * //Users/%s/ShareWithOtherUsers/...' % (name, name)),
            str('write user %s * //Users/%s/ShareWithStaff/...' % (name, name)),
            str('write group %s * //Users/%s/ShareWithOtherUsers/...' % ('Users', name)),
            str('write group %s * //Users/%s/ShareWithStaff/...' % ('Staff', name)),
        ]
    return protect_lines


def update_p4_protect_for_users():

    with P4Connection('localhost', '1666', 'kalms') as p4:

        protections = p4.read_protect()
        from models import MetaUser
        for meta_user in MetaUser.objects.all():
            if meta_user.ldap_user and meta_user.p4_user:
                p4_user = meta_user.p4_user

                user_protect_lines = generate_protect_lines_for_user(p4_user.user)

                for user_protect_line in user_protect_lines:
                    if not user_protect_line in protections:
                        protections.append(user_protect_line)

        p4.write_protect(protections)


def create_student_user_in_p4(p4, login, email, fullname):

        p4.create_user(login, email, fullname)
        p4.add_user_to_group(login, 'Users')
        p4.add_user_to_group(login, 'Students')

def create_student_standard_files_in_p4(p4, user):

        local_prefix = 'WorkspaceTemplates/NewUser/'
        depot_prefix = '//Users/%s/' % user

        for root, dirs, files in os.walk(local_prefix):
            for file in files:
                file_with_local_prefix = root + '/' + file
                print file_with_local_prefix
                file_without_local_prefix = file_with_local_prefix[len(local_prefix):]
                local_file = local_prefix + file_without_local_prefix
                depot_file = depot_prefix + file_without_local_prefix
                p4.import_local_file(local_file, depot_file, 'Setting up user-area for %s' % user)

def create_protect_lines_for_user_in_p4(p4, user):

        protections = p4.read_protect()

        user_protect_lines = generate_protect_lines_for_user(user)

        for user_protect_line in user_protect_lines:
            if not user_protect_line in protections:
                protections.append(user_protect_line)

        p4.write_protect(protections)

def setup_student_in_p4(p4, login, email, fullname):

    create_student_user_in_p4(p4, login, email, fullname)
    create_student_standard_files_in_p4(p4, login)
    create_protect_lines_for_user_in_p4(p4, login)
