from uuid import UUID
from typing import List
from asgiref.sync import sync_to_async
from typing import Type, TypeVar

from pydantic import BaseModel
from django.db import models

ModelType = TypeVar("ModelType", bound=models.Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)


class BaseService:
    """ `BaseService` base class for services
    """
    model: Type[ModelType]
    create_schema: CreateSchemaType
    update_schema: UpdateSchemaType
    get_schema: GetSchemaType

    def update(self, pk: UUID, schema, **kwargs) -> ModelType:
        obj = self.model.objects.get(id=pk)

        for key, value in schema.items():
            setattr(obj, key, value)

        for key, value in kwargs.items():
            setattr(obj, key, value)

        obj.save()
        return obj

    def get(self, **kwargs) -> ModelType:
        try:
            obj = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            obj = None
        return obj

    @sync_to_async
    def async_get(self, **kwargs) -> ModelType:
        return self.get(**kwargs)

    def get_list(self, **kwargs) -> List[ModelType]:
        obj_list = self.model.objects.filter(**kwargs).all()
        return obj_list

    def delete(self, **kwargs) -> None:
        try:
            obj = self.model.objects.get(**kwargs)
            obj.delete()
        except self.model.DoesNotExist:
            return None
