from django.db import models
import re

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters'
        
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'

        # add uniqueness check for email, doesn't already exist
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['duplicate'] = 'Email already registered'

        if len(postData['password']) < 8 or len(postData['pw_confirm']) < 8:
            errors['pw_length'] = 'Password must be at least 8 characters'

        if postData['password'] != postData['pw_confirm']:
            errors['pw_match'] = 'Passwords do not match'

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 128)
    last_name = models.CharField(max_length = 128)

    email = models.CharField(max_length = 256)

    # config password input field; 60 max length?
    pw_hash = models.CharField(max_length = 64)

    # UserManager() will need to come in
    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)