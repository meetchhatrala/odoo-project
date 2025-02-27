# from rest_framework import serializers
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'name', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user


# 

# from rest_framework import serializers
# from bson import ObjectId  # Import for handling MongoDB ObjectId
# from .models import User  # Import your User model

# class UserSerializer(serializers.ModelSerializer):
#     id = serializers.CharField(read_only=True)  # Directly handle ObjectId as a string

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'name', 'password']  # Removed 'username'
#         extra_kwargs = {'password': {'write_only': True}}  # Ensure password isn't exposed

#     def to_representation(self, instance):
#         """ Convert ObjectId to string for JSON response """
#         representation = super().to_representation(instance)
#         representation['id'] = str(instance.id) if isinstance(instance.id, ObjectId) else instance.id
#         return representation


from rest_framework import serializers
from bson import ObjectId
from .models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}  

    def create(self, validated_data):
        """ Hash password before saving user """
        user = User(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def to_representation(self, instance):
        """ Convert ObjectId to string for JSON response """
        representation = super().to_representation(instance)
        representation['id'] = str(instance.id) if isinstance(instance.id, ObjectId) else instance.id
        return representation
