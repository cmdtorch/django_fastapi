from pydantic import ConfigDict, BaseModel
from pydantic import model_validator, root_validator

config = ConfigDict(from_attributes=True)


class BaseSchema(BaseModel):
    model_config = config

    @model_validator(mode='before')
    @classmethod
    def fields_t(cls, instance):
        data = {}
        for name, info in cls.model_fields.items():
            try:
                field_type = info.annotation.__args__[0]
            except AttributeError:
                field_type = info.annotation

            if issubclass(field_type, BaseModel):
                if name in instance._state.fields_cache:
                    data[name] = instance._state.fields_cache[name]
                elif hasattr(instance, '_prefetched_objects_cache'):
                    values = instance._prefetched_objects_cache.get(name, None)
                    data[name] = values
                else:
                    data[name] = None
            else:
                data[name] = getattr(instance, name)
        return data
