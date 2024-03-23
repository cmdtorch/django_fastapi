import datetime
import re

from django.db.models import DateField, DateTimeField
from pydantic import ConfigDict, BaseModel
from pydantic import model_validator, root_validator
from django.db.models.fields.files import FieldFile, ImageField
from django.conf import settings

config = ConfigDict(from_attributes=True)

media_path = settings.MEDIA_SRC


class BaseSchema(BaseModel):
    model_config = config

    @model_validator(mode='before')
    @classmethod
    def fields_t(cls, instance):
        if isinstance(instance, dict):
            return instance
        data = {}
        for name, info in cls.model_fields.items():
            try:
                field_type = info.annotation.__args__[0]
            except AttributeError:
                field_type = info.annotation
            # Relations
            if issubclass(field_type, BaseModel):
                if name in instance._state.fields_cache:
                    data[name] = instance._state.fields_cache[name]
                elif hasattr(instance, '_prefetched_objects_cache'):
                    values = instance._prefetched_objects_cache.get(name, None)
                    data[name] = values
                else:
                    data[name] = None
            # Files
            elif isinstance(getattr(instance, name), (FieldFile, ImageField)):
                data[name] = getattr(instance, name)
                if not getattr(instance, name):
                    return None
                value = getattr(instance, name).url
                data[name] = re.sub(f'.*{media_path}', media_path, value)
            # Dates
            # elif isinstance(getattr(instance, name), datetime.datetime):
            #     data[name] = getattr(instance, name).strftime("%m/%d/%Y, %H:%M:%S")
            # elif isinstance(getattr(instance, name), datetime.date):
            #     data[name] = getattr(instance, name).strftime("%m/%d/%Y")
            # Other
            else:
                data[name] = getattr(instance, name)
        return data
