from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async


# class TokenAuthMiddleware:
#     """
#     Token authorization middleware for Django Channels 2
#     """

#     def __init__(self, inner):
#         self.inner = inner

#     async def __call__(self, scope):
#         headers = dict(scope['headers'])
#         print(headers)
#         if b'authorization' in headers:
#             try:
#                 token_name, token_key = headers[b'authorization'].decode().split()
#                 if token_name == 'Token':
#                     token = await database_sync_to_async(Token.objects.get)(key=token_key)
#                     scope['user'] = token.user
#             except Token.DoesNotExist:
#                 scope['user'] = AnonymousUser()
#         return await self.inner(scope)

# TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

@database_sync_to_async
def get_user(token_key):
    try:
        return Token.objects.get(key=token_key).user
    except Token.DoesNotExist:
        return AnonymousUser()
# @database_sync_to_async
# def get_user(token_key):
#     try:
#         return get_user_model().objects.get(auth_token__key=token_key)
#     except get_user_model().DoesNotExist:
#         return AnonymousUser()



class TokenAuthMiddlewareInstance:
    """
    Token authorization middleware for Django Channels 3
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        headers = dict(self.scope['headers'])
        print(headers)
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name == 'Token':
                self.scope['user'] = await get_user(token_key)
        inner = self.inner(self.scope)
        return await inner(receive, send)

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
