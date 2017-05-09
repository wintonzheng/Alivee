# Put Third Party/Django Imports Here:
from django.db import models


class TruncatingCharField(models.CharField):
    '''
    Define a truncating charField for model usage.
    '''
    def get_prep_value(self, value):
        value = super(TruncatingCharField, self).get_prep_value(value=value)
        if value:
            if len(value) > self.max_length:
                print 'Value {} length > {} truncating...'.format(value, self.max_length)

            return value[:self.max_length]

        return value


class ValidationMixin(object):
    '''
    Extend this model and define a `full_clean()` function, so we can have pre-save validation.
    '''
    def save(self, *args, **kwargs):
        self.full_clean()
        super(ValidationMixin, self).save(*args, **kwargs)
