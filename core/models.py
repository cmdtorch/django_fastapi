import uuid
from django.db import models
from starlette_context.errors import ContextDoesNotExistError
from starlette_context import context


class BaseClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, blank=True)

    class Meta:
        abstract = True


class BaseClassLang(BaseClass):
    lang_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.lang_fields:
            try:
                self.__init_lang()
            except ContextDoesNotExistError:
                pass

    def __init_lang(self):
        for field in self.lang_fields:
            if hasattr(self, field) and getattr(self, field) is not None:
                try:
                    setattr(self, field, getattr(self, f"{field}_{context['lang']}"))
                except KeyError:
                    setattr(self, field, getattr(self, f"{field}_en"))

    class Meta:
        abstract = True
