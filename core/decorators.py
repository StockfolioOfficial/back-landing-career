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