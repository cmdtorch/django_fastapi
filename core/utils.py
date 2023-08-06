from fastapi import Header
from typing import Optional
from starlette_context import context


async def get_language(lang_code: Optional[str] = Header(None)):
    if lang_code is not None and lang_code != '':
        context['lang'] = lang_code
        return lang_code
    else:
        context['lang'] = 'en'
        return 'en'
