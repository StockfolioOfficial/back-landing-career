import jwt

from django.http  import JsonResponse

from users.models       import User
from global_variable    import SECRET_KEY, ALGORITHM

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

def admin_only(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            pay_load     = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            role         = pay_load['role']
            user         = User.objects.get(id=pay_load['user_id'])
            request.user = user
            
            if role == 'admin' or role == 'superadmin':
                return func(self, request, *args, **kwargs)
            else:
                return JsonResponse({'message': 'UNAUTHORIZED'}, status=401)

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

def superadmin_only(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            pay_load     = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            role         = pay_load['role']
            user         = User.objects.get(id=pay_load['user_id'])
            request.user = user
            
            if not role == 'superadmin':
                return JsonResponse({'message': 'UNAUTHORIZED'}, status=401)

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