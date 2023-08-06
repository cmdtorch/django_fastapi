# FastApi - Django

----

This is a simple bundle of two frameworks Django and FastAPI. To combine the best of two frameworks. Django admin panel and simple ORM with api routing and schemas FastAPI.

## Installation

----
Clone repository
```bash
$ git clone https://github.com/Emil4154515/django_fastapi
```
Install packages
```bash
$ pip install -r requirements.txt
```

## Until run

----

Migration
```bash
python manage.py migrate
```

## ORM Usage

----
###Simple Usage
```python
from datetime import datetime
from fastapi import APIRouter
from django.contrib.auth.models import User

from core.schema import BaseSchema

class DjangoUserSchema(BaseSchema):
    username: str
    first_name: str
    last_name: str
    email: str
    date_joined: datetime

user_router = APIRouter()

@user_router.get('/user/', response_model=DjangoUserSchema)
def get_user():
    return User.objects.first()
```

###Relation fields
`models.py`
```python
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')

    def __str__(self):
        return self.headline
```
`api.py`
```python
from datetime import datetime
from typing import Optional
from fastapi import APIRouter
from django.contrib.auth.models import User

from core.schema import BaseSchema
from .models import Article

class DjangoUserSchema(BaseSchema):
    username: str
    first_name: str
    last_name: str
    email: str
    date_joined: datetime
    
class ArticleSchema(BaseSchema):
    headline: str
    pub_date: datetime
    reporter: Optional[DjangoUserSchema] = None

article_router = APIRouter()

@article_router.get('/article_with_user/', response_model=ArticleSchema)
def get_article_with_user():
    """
    Use `select_related` or `prefetch_related` for relation fields 
    """
    return Article.objects.select_realted('reporter').first()

@article_router.get('/article/', response_model=ArticleSchema)
def get_article():
    """
    `reporter` will be None
    """
    return Article.objects.first()
```



## Run

----
```bash
$ uvicorn mysite.app:fastapp --port 8000 --reload
...
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
...
```