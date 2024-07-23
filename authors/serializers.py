from django.contrib.auth import get_user_model
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta: 
        extra_kwargs = {
        'password': {'write_only': True}
        }
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        self.validate_first_name(attrs.get('first_name'))
        self.validate_last_name(attrs.get('last_name'))
        self.validate_email(attrs.get('email'))
        my_errors = dict()
        password = attrs.get('password')
        if password == '' or password is None:
            my_errors['password'] = ['Insira uma senha']
        if my_errors:
            raise serializers.ValidationError(my_errors)
    
        return super_validate
    
    def validate_first_name(self, valor):
        print(valor)
        if valor == '' or valor is None:
            raise serializers.ValidationError('The field first_name cannot be left blank')
        return valor
    
    def validate_last_name(self, valor):
        if valor == '' or valor is None:
            raise serializers.ValidationError('The field first_name cannot be left blank')
        return valor
    
    def validate_email(self, valor):
        if valor == '' or valor is None:
            raise serializers.ValidationError('The field first_name cannot be left blank')
        return valor