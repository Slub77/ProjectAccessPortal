
from P4Connection import P4Connection

from p4_modify import update_p4_protect_for_projects, create_project_standard_files_in_p4

from models import P4Group, MetaProject

def add_user_to_project(meta_project, meta_user):

    # Add user to group in P4
    # Add user to P4Group
    # Add user to MetaProject

    with P4Connection('localhost', '1666', 'kalms') as p4:
        p4.add_user_to_group(meta_project.p4_group.name, str(meta_user.p4_user.user))
        meta_project.members.add(meta_user)

def remove_user_from_project(meta_project, meta_user):

    # Remove user from group in P4
    # Remove user from P4Group
    # Remove user from MetaProject

    with P4Connection('localhost', '1666', 'kalms') as p4:
        p4.remove_user_from_group(meta_project.p4_group.name, meta_user.p4_user.user)
        meta_project.members.remove(meta_user)

def create_new_project(project_block, project_name):

    p4_group_name = 'Project-%s-%s' % (project_block, project_name)
    p4_project_root = '//Projects/%s/%s/' % (project_block, project_name)

    with P4Connection('localhost', '1666', 'kalms') as p4:
        # Add default project user to group in P4
        p4.add_user_to_group(p4_group_name, 'default_project_user')

        # If no manual checkins have been made, create starter file structure
        if not p4.file_exists(p4_project_root + '...'):
            create_project_standard_files_in_p4(p4, p4_project_root)
        # Create workspace template
        # Add group to P4Groups
        p4_group = P4Group.objects.create(name=p4_group_name)
        # Create MetaProject; Add P4Group to MetaProject
        meta_project = MetaProject.objects.create(block=project_block, name=project_name, p4_group=p4_group)

        # Update protections
        # NOTE: must happen after meta project has been configured;
        # TODO: make this not depend on MetaProjects?
        update_p4_protect_for_projects()

        # Return MetaProject
        return meta_project

def delete_project(meta_project):

    with P4Connection('localhost', '1666', 'kalms') as p4:
        # Delete group in P4
        p4.delete_group(meta_project.p4_group.name)
        # Update protections
        update_p4_protect_for_projects()
        # Delete workspace template
        # If "force", delete project content in P4
        # Delete P4Group
        meta_project.p4_group.delete()
        # Delete MetaProject
        meta_project.delete()

    pass
