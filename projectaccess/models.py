from django.db import models

from django.contrib.auth.models import User

# Example of an LDAP user entry (this has been extracted from an example .ldif file)
#
## rdaugherty, People, example.com
# dn: uid=rdaugherty,ou=People,dc=example,dc=com
# objectClass: person
# objectClass: inetOrgPerson
# objectClass: organizationalPerson
# objectClass: posixAccount
# objectClass: top
# uid: rdaugherty
# userPassword:: YXBwbGVz
# facsimileTelephoneNumber: +1 408 555 1992
# givenName: Robert
# cn: Robert Daugherty
# telephoneNumber: +1 408 555 1296
# sn: Daugherty
# roomNumber: 0194
# homeDirectory: /home/rdaugherty
# mail: rdaugherty@example.com
# l: Sunnyvale
# ou: Human Resources
# ou: People
# uidNumber: 1014
# gidNumber: 1000

# Example of a P4 user specification
#
# User: rdaugherty
#
# Email: rdaugherty@example.com
#
# FullName: Robeert Daugherty

class PAUser(models.Model):
    name = models.CharField("Name", max_length=1024)
    p4_user_name = models.CharField("P4UserName", max_length=1024)

class LDAPUser(models.Model):
    dn = models.CharField("dn", max_length=1024)
    pa_user = models.OneToOneField(PAUser, null=True)

class UserProfile(models.Model):
    pa_user = models.OneToOneField(PAUser, null=True)

class PAGroup(models.Model):
    name = models.CharField("Name", max_length=1024)
    members = models.ManyToManyField(PAUser)

class PAProject(models.Model):
    name = models.CharField("Name", max_length=1024)
    p4_path = models.CharField("P4Path", max_length=1024)
    p4_access_group_name = models.CharField("P4AccessGroupName", max_length=1024)
    # TODO: add support for giving groups access

class PAUserProjectAccess(models.Model):
    project = models.ForeignKey(PAProject)
    user = models.ForeignKey(PAUser)
    # TODO: add access mode (read/write or read-only)

class PAGroupProjectAccess(models.Model):
    project = models.ForeignKey(PAProject)
    group = models.ForeignKey(PAGroup)
    # TODO: add access mode (read/write or read-only)
