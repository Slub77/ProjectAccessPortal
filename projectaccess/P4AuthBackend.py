from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from P4Connection import P4Connection

import logging
logger = logging.getLogger(__name__)

class P4AuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, username=None, password=None):
        try:
            with P4Connection('localhost', '1666', str(username)) as p4:
                pass

        except Exception, e:
            logger.info("Perforce authentication failed for user %s with message %s" % (username, e.message))
            return None

        try:
            return User.objects.get(username=username)
        except:
            user = User.objects.create(username=username)
            user.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
