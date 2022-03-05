from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','username','password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self,validate_data):
        password=validate_data.pop('password',None)
        #instance.name=validate_data.get('name',instance.name)
        #instance.username=validate_data.get('username',instance.username)
        #instance.email=validate_data.get('email,instance.email)
    
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


