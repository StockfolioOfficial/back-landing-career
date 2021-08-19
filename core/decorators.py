import jwt

from django.http import JsonResponse

from users.models import User

from my_settings import SECRET_KEY, ALGORITHM

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            pay_load     = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            user         = User.objects.get(id=pay_load['user_id'])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=400)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXISTS'}, status=401)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    return wrapper

import functools, time
from django.db import connection, reset_queries

def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        number_of_end_queries = len(connection.queries)
        print(f"-------------------------------------------------------------------")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        print(f"-------------------------------------------------------------------")
        return result
    return wrapper