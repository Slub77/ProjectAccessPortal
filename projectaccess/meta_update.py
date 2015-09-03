
from models import P4User, LDAPUser, MetaUser, P4Group, MetaProject

import logging
logger = logging.getLogger(__name__)

def clear_meta_users():
    MetaUser.objects.all().delete()

# List all LDAP and P4 users, and concile them into meta-users

def construct_meta_users_from_real_users():

    remaining_ldap_users = {}
    remaining_p4_users = {}

    meta_users = []

    for ldap_user in LDAPUser.objects.all():
        remaining_ldap_users[ldap_user.dn] = True

    for p4_user in P4User.objects.all():
        remaining_p4_users[p4_user.user] = True

    ldap_users_used = {}
    p4_users_used = {}
    for ldap_user_dn in remaining_ldap_users:
        ldap_user = LDAPUser.objects.get(dn=ldap_user_dn)

        try:
            p4_user=P4User.objects.get(user=ldap_user.uid)
            meta_users.append((ldap_user, p4_user))
            ldap_users_used[ldap_user.dn] = True
            p4_users_used[p4_user.user] = True
        except:
            pass

    for ldap_user_dn in ldap_users_used:
        del remaining_ldap_users[ldap_user_dn]

    for p4_user_user in p4_users_used:
        del remaining_p4_users[p4_user_user]

    for ldap_user_dn in remaining_ldap_users:
        ldap_user = LDAPUser.objects.get(dn=ldap_user_dn)
        meta_users.append((ldap_user, None))

    for p4_user_user in remaining_p4_users:
        p4_user=P4User.objects.get(user=p4_user_user)
        meta_users.append((None, p4_user))

    return meta_users

# Update the Meta user object set based on LDAP and P4 user object sets

def update_meta_users():

    new_meta_users = construct_meta_users_from_real_users()

    def create(new_meta_users):
        for (ldap_user, p4_user) in new_meta_users:

            try:
                MetaUser.objects.get(ldap_user=ldap_user, p4_user=p4_user)
            except:
                meta_user = MetaUser.objects.create(ldap_user=ldap_user, p4_user=p4_user)
                logger.info("Creating Django model for meta user " + str(meta_user))
                meta_user.save()

    create(new_meta_users)

    def remove(new_meta_users):

        users_to_keep = {}
        for (ldap_user, p4_user) in new_meta_users:
            users_to_keep[MetaUser.hash(ldap_user, p4_user)] = True

        for old_meta_user in MetaUser.objects.all():
                if not MetaUser.hash(old_meta_user.ldap_user, old_meta_user.p4_user) in users_to_keep:
                    logger.info("Removing Django model for meta user " + str(old_meta_user))
                    old_meta_user.delete()

    remove(new_meta_users)


def update_meta_projects():

    project_name_prefix = 'Project-'

    def p4_group_name_to_project_block_and_name(name):
        if not name.startswith(project_name_prefix):
            raise Exception("All P4 groups which are to be made projects must begin with " + project_name_prefix)
        block_and_name = name[len(project_name_prefix):]
        (project_block, project_name) = block_and_name.split('-', 1)
        return (project_block, project_name)

    def project_block_and_name_to_p4_group_name(project_block, project_name):
        return '%s%s-%s' % (project_name_prefix, project_block, project_name)

    new_p4_project_groups = [(p4_group, p4_group_name_to_project_block_and_name(p4_group.name)) \
                             for p4_group in P4Group.objects.all() if p4_group.name.startswith("Project-")]

    def add(new_p4_project_groups):
        for (p4_project_group, (project_block, project_name)) in new_p4_project_groups:
            try:
                MetaProject.objects.get(block=project_block, name=project_name)
            except:
                meta_project = MetaProject.objects.create(block=project_block, name=project_name)
                logger.info("Creating Django model for meta project %s - %s" % (project_block, project_name))
                meta_project.save()

    def update(new_p4_project_groups):
        for (p4_project_group, (project_block, project_name)) in new_p4_project_groups:
            meta_project = MetaProject.objects.get(block=project_block, name=project_name)

            def add_users(meta_project, p4_project_group):
                modified = False
                for p4_user in p4_project_group.member_users.all():
                    meta_user = MetaUser.objects.get(p4_user=p4_user)

                    if not meta_project.members.filter(id=meta_user.id).exists():
                        meta_project.members.add(meta_user)
                        modified = True

                return modified

            def remove_users(meta_project, p4_project_group):
                modified = False

                for meta_user in list(meta_project.members.all()):
                    if not p4_project_group.member_users.filter(id=meta_user.p4_user.id).exists():
                        meta_project.members.remove(meta_user)
                        modified = True

                return modified

            def update_p4_group(meta_project, p4_project_group):
                if meta_project.p4_group != p4_project_group:
                    meta_project.p4_group = p4_project_group
                    return True
                else:
                    return False

            modified = add_users(meta_project, p4_project_group)
            modified = modified or remove_users(meta_project, p4_project_group)
            modified = modified or update_p4_group(meta_project, p4_project_group)

            if modified:
                logger.info("Updating Django model for meta project %s - %s" % (project_block, project_name))
                meta_project.save()


    def remove(new_p4_project_groups):

        meta_projects_to_keep = {}
        for (p4_project_group, (project_block, project_name)) in new_p4_project_groups:
            meta_projects_to_keep[p4_project_group.name] = True

        for old_meta_project in MetaProject.objects.all():
                if not project_block_and_name_to_p4_group_name(old_meta_project.block, old_meta_project.name) in meta_projects_to_keep:
                    logger.info("Removing Django model for meta project %s - %s" % (old_meta_project.block, old_meta_project.name))
                    old_meta_project.delete()

    add(new_p4_project_groups)
    update(new_p4_project_groups)
    remove(new_p4_project_groups)


def clear_meta_projects():
    MetaProject.objects.all().delete()

def update_all_meta_users_and_projects():
#    clear_meta_users()
#    clear_meta_projects()

    update_meta_users()
    update_meta_projects()
