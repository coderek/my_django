from django.db import models


class Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    @classmethod
    def all(cls):
        return [
            m.as_dict()
            for m in cls.objects.all()
        ]
