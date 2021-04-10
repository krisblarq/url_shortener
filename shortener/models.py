from hashlib import sha256

from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from graphql import GraphQLError


class URL(models.Model):
    full_url = models.URLField(unique=True)
    url_hash = models.URLField(unique=True)
    

    def save(self, *args, **kwargs):
        self.url_hash = sha256(self.full_url.encode()).hexdigest()[:6]

        validate = URLValidator()
        try:
            validate(self.full_url)
        except ValidationError as e:
            raise GraphQLError('Invalid url')

        return super().save(*args, **kwargs)
