from starlette.middleware import Middleware
from starlette_context.middleware import ContextMiddleware
from starlette_context import plugins


middleware = [
    Middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin()
        )
    )
]
