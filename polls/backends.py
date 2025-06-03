from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, identifier, password, **kwargs):
        users = UserModel.objects.filter(email=identifier) 

        if not users.exists(): 
            users = UserModel.objects.filter(phone_number=identifier)

        if not users.exists():
            return None  

        user = users.first() 
        if user.check_password(password):
            return user
        return None
