from django.db import models
from login_app.models import User

class GroupManager(models.Manager):
    def group_validator(self,postData):
        errors = {}

        if len(postData['org_name']) <= 0:
            errors['org_name_empty'] = "Organization name cannot be empty"

        if len(postData['org_name']) < 5:
            errors['org_name_short'] = "Organization name must be at least 5 characters long"

        if len(postData['desc']) < 10:
            errors['desc_short'] = "Organization description must be at least 10 characters long"

        if Group.objects.filter(org_name=postData['org_name']).count() > 0:
            errors['duplicate'] = "Organization with this name already exists"

        return errors

class Group(models.Model):
    org_name = models.CharField(max_length = 64)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='groups_created', on_delete = models.CASCADE)
    members = models.ManyToManyField(User, related_name='groups')

    objects = GroupManager()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)