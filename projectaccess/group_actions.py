
from django.conf import settings

from P4Connection import P4ConnectionAsServiceUser
from models import PAUser, PAGroup

import logging
logger = logging.getLogger(__name__)

def create_new_group(group_name):

    group = PAGroup.objects.create(name=group_name)
    group.save()

    return group

def delete_group(group):

    if settings.PERFORCE_INTEGRATION_ENABLED:
        with P4ConnectionAsServiceUser() as p4:

            # Delete group in P4
            # TODO: perhaps check for group existence before deleting? That will allow for ignoring a narrower range of exceptions
            try:
                    p4.delete_group(group.name)
            except:
                pass

    group.delete()

    pass

def add_user_to_group(group, user):

    group.members.add(user)
    group.save()

    if settings.PERFORCE_INTEGRATION_ENABLED:
        with P4ConnectionAsServiceUser() as p4:
            p4.add_user_to_group(str(group.name), str(user.p4_user_name))

def remove_user_from_group(group, user):

    group.members.remove(user)
    group.save()
    if settings.PERFORCE_INTEGRATION_ENABLED:
        with P4ConnectionAsServiceUser() as p4:
            p4.remove_user_from_group(str(group.name), str(user.p4_user_name))
