
from p4access import P4Connection
from models import P4User, P4Group

import os

import logging
logger = logging.getLogger(__name__)

def clear_p4_users():
    P4User.objects.all().delete()

def update_p4_users(new_p4_users):

    def create(new_p4_users):
        for new_p4_user in new_p4_users:
            user = new_p4_user['User']
            try:
                P4User.objects.get(user=user)
            except:
                logger.info("Creating Django model for P4 user " + user)
                p4_user = P4User.objects.create(user=user)
                p4_user.save()

    create(new_p4_users)

    def update(new_p4_users):
        for new_p4_user in new_p4_users:
            user = new_p4_user['User']
            try:
                old_p4_user = P4User.objects.get(user=user)

                if (old_p4_user.email != new_p4_user_details['Email'] \
                    or old_p4_user.full_name != new_p4_user_details['FullName']):

                    logger.info("Updating Django model for P4 user " + user)
                    old_p4_user.email = new_p4_user_details['Email']
                    old_p4_user.full_name = new_p4_user_details['FullName']
                    old_p4_user.save()
            except:
                pass

    update(new_p4_users)

    def remove(new_p4_users):
        users_to_keep = {}
        for new_p4_user in new_p4_users:
            users_to_keep[new_p4_user['User']] = True

        for old_p4_user in P4User.objects.all():
                if not old_p4_user.user in users_to_keep:
                    logger.info("Removing Django model for P4 user " + old_p4_user.user)
                    old_p4_user.delete()

    remove(new_p4_users)

def update_p4_groups(new_p4_groups):

    def create(new_p4_groups):
        for group_name in new_p4_groups:
            try:
                P4Group.objects.get(name=group_name)
            except:
                logger.info("Creating Django model for P4 group " + group_name)
                p4_group = P4Group.objects.create(name=group_name)
                p4_group.save()

    create(new_p4_groups)

    def remove(new_p4_groups):
        groups_to_keep = {}
        for group_name in new_p4_groups:
            groups_to_keep[group_name] = True

        for old_p4_group in P4Group.objects.all():
                if not old_p4_group.name in groups_to_keep:
                    logger.info("Removing Django model for P4 group " + old_p4_group.name)
                    old_p4_group.delete()

    remove(new_p4_groups)

    def update_membership(new_p4_groups):
        for group_name, (group_users, group_subgroups) in new_p4_groups.iteritems():

            old_p4_group = P4Group.objects.get(name=group_name)

            def add_users(old_p4_group, group_users):
                old_member_users = old_p4_group.member_users.all()

                modified = False
                for user in group_users:
                    p4_user = P4User.objects.get(user=user)
                    if not p4_user in old_member_users:
                        old_p4_group.member_users.add(p4_user)
                        modified = True

                return modified

            def remove_users(old_p4_group, group_users):
                modified = False

                for p4_user in old_p4_group.member_users.all():
                    if not p4_user.user in group_users:
                        old_p4_group.member_users.remove(p4_user)
                        modified = True

                return modified

            def add_subgroups(old_p4_group, group_subgroups):
                old_member_subgroups = old_p4_group.member_subgroups.all()

                modified = False
                for subgroup in group_subgroups:
                    p4_subgroup = P4Group.objects.get(group=subgroup)
                    if not p4_subgroup in old_member_subgroups:
                        old_p4_group.member_subgroups.add(p4_subgroup)
                        modified = True

                return modified

            def remove_subgroups(old_p4_group, group_subgroups):
                modified = False

                for p4_subgroup in old_p4_group.member_subgroups.all():
                    if not p4_subgroup.name in group_subgroups:
                        old_p4_group.member_subgroups.remove(p4_subgroup)
                        modified = True

                return modified

            modified = add_users(old_p4_group, group_users)
            modified = modified or remove_users(old_p4_group, group_users)
            modified = modified or add_subgroups(old_p4_group, group_subgroups)
            modified = modified or remove_subgroups(old_p4_group, group_subgroups)

            if modified:
                old_p4_group.save()

    update_membership(new_p4_groups)

def updatep4():
#    clear_p4_users()

    with P4Connection('localhost', '1666', 'kalms') as p4:
        current_p4_users = p4.get_users()
        current_p4_group_names = [group['group'] for group in p4.get_groups()]
        current_p4_groups = {}
        for group in current_p4_group_names:
            current_p4_groups[group] = p4.read_group_members(group)

    update_p4_users(current_p4_users)
    update_p4_groups(current_p4_groups)

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
