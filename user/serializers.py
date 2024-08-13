from .models import NewUser, Profile
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers



class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    d_o_b = serializers.CharField(required=False)
    phone_no = serializers.CharField(required=False)
    upload_id = serializers.ImageField(required=False)
    address = serializers.CharField(required=False)
    class Meta:
        model= Profile        
        fields = ('avatar', 'd_o_b', 'phone_no', 'address', 'upload_id',)

class NewUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = NewUser
        fields = ('id', 'email', 'first_name', 'last_name', 'tag', 'middle_name', 'full_name', 'profile')

    
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    middle_name = serializers.CharField(required=False)
    tag = serializers.CharField(read_only=True)
    profile = ProfileSerializer(required=False)
    d_o_b = serializers.DateField(required=False)
    phone_no = serializers.CharField(required=False)
    address = serializers.CharField(required=False, write_only=True)
    upload_id = serializers.ImageField(required=False, write_only=True)
    class Meta:
        model = NewUser
        fields = ('id','email','password', 'password2',  'first_name', 'last_name', 'middle_name', 'tag', 'd_o_b', 'phone_no', 'profile',
                  'upload_id', 'address')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError({ "password": "Password fields didn't match." })

        return attrs


    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        address = validated_data.pop('address', None)
        d_o_b = validated_data.pop('d_o_b', None)
        phone_no = validated_data.pop('phone_no', None)
        upload_id = validated_data.pop('upload_id', None)
        password = validated_data.get('password')
        user = NewUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        if upload_id is not None and address is not None:
            try:
                profile = Profile.objects.create(user=user)
                profile.address = address
                profile.d_o_b=d_o_b
                profile.phone_no=phone_no
                profile.upload_id=upload_id
                profile.save()
            except Exception as e:
                raise Exception(str(e))
        if profile_data:
            profile = Profile.objects.create(user=user, **profile_data)

        return user   

class UpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    middle_name = serializers.CharField(required=False)
    d_o_b = serializers.DateField(required=False)
    profile= ProfileSerializer(required=False)
    avatar = serializers.ImageField(required=False, write_only=True)
    phone_no = serializers.CharField(required=False, write_only=True)
    address = serializers.CharField(required=False, write_only=True)
    upload_id = serializers.ImageField(required=False, write_only=True)
    class Meta:
        model = NewUser
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'd_o_b', 'profile', 'avatar', 'upload_id', 'phone_no', 'address')
        
    def update(self, instance, validated_data):
        address = validated_data.pop('address', None)
        upload_id = validated_data.pop('upload_id', None)
        avatar = validated_data.pop('avatar', None)
        phone_no = validated_data.pop('phone_no', None)
        d_o_b = validated_data.pop('d_o_b', None)
        
        mob_pro = {
            'avatar': avatar,
            'upload_id' : upload_id, 
            'phone_no': phone_no, 
            'd_o_b': d_o_b,
            'address' : address
        }
       
        profile_data = validated_data.pop('profile', None)
        profile = instance.profile
        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
       
        # Update UserProfile fields
        if profile_data:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        try:
            for attr, value in mob_pro.items():
                if value:
                    setattr(profile, attr, value)
            profile.save()
        except Exception as e:
            raise Exception(str(e))

        return instance   

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = NewUser
        fields = ( 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, data):
        user = authenticate(**data)
        
        if user is None:
            raise serializers.ValidationError("Email or password is incorrect.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive. Please activate your account.")
        
        return user