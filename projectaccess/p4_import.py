
from p4access import P4Connection
from models import P4User, P4Group

import logging
logger = logging.getLogger(__name__)

def clear_django_users():
    P4User.objects.all().delete()

def update_django_users(new_p4_users):

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

def update_django_groups(new_p4_groups):

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

def import_p4_to_django():
#    clear_django_users()

    with P4Connection('localhost', '1666', 'kalms') as p4:
        current_p4_users = p4.get_users()
        current_p4_group_names = [group['group'] for group in p4.get_groups()]
        current_p4_groups = {}
        for group in current_p4_group_names:
            current_p4_groups[group] = p4.read_group_members(group)

    update_django_users(current_p4_users)
    update_django_groups(current_p4_groups)

