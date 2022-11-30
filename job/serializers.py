from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from job.models import (
    Applicant,
    ApplicantSkill,
    ApplicantEducation,
    ApplicantExperience,
    JobApplication,
    JobPost
)


class UserSerializer(serializers.ModelSerializer):
    """A serializer for the user model."""

    class Meta:
        model = User
        fields = '__all__'


class UserMinimalSerializer(serializers.ModelSerializer):
    """A serializer for the user model."""
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class LoginSerializer(serializers.Serializer):
    """ A serializer for logging in."""
    username = serializers.CharField(
        max_length=100,
        style={'placeholder': 'Username', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'A username is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Invalid username/password!'
            )
        return data


class JobPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPost
        fields = '__all__'
        read_only = ['id']


class ApplicantSerializer(serializers.ModelSerializer):
    """A serializer for the applicant. """
    user = UserMinimalSerializer()

    class Meta:
        model = Applicant
        fields = ['user', 'firstname', 'secondname', 'email', 'relocation']
        read_only = ['id']

    def create(self, validated_data):
        user = {
            'username' : validated_data["user"]["username"],
            'password' : make_password(validated_data["user"]["password"])
        }
        user_created = User.objects.create(**user)
        applicant_ = {
            'user': user_created,
            'firstname': validated_data["firstname"],
            'secondname': validated_data["secondname"],
            'email': validated_data["email"],
            'relocation': validated_data["relocation"]
        }
        applicant_data = Applicant.objects.create(**applicant_)

        return applicant_data


class ApplicantExperienceSerializer(serializers.ModelSerializer):
    """A serializer for the applicant experience."""

    class Meta:
        model = ApplicantExperience
        fields = ['is_current', 'start_date', 'end_date', 'job_title', 'company_name',
                  'job_location', 'description']
        read_only = ['id']


class ApplicantEducationSerializer(serializers.ModelSerializer):
    """A serializer for the applicant education."""

    class Meta:
        model = ApplicantEducation
        fields = ['certification_awarded', 'education_level', 'institution_name',
                  'start_date', 'end_date', 'grade']
        read_only = ['id']


class ApplicantSkillSerializer(serializers.ModelSerializer):
    """A serializer for the applicant skill."""

    class Meta:
        model = ApplicantSkill
        fields = ['applicant', 'skill', 'skill_level']
        read_only = ['id']


class JobApplicationSerializer(serializers.ModelSerializer):
    """A serializer for the job application"""
    applicant_experience = ApplicantExperienceSerializer()
    applicant_education = ApplicantEducationSerializer()
    applicant_skill = ApplicantSkillSerializer()

    class Meta:
        model = JobApplication
        fields = ['applicant_experience', 'applicant_education', 'applicant_skill', 'jobpost']
        read_only = ['id', 'created_by', ]

    def create(self, validated_data):
        applicant_experience = {
            'is_current': validated_data["applicant_experience"]["is_current"],
            'start_date': validated_data["applicant_experience"]["start_date"],
            'end_date': validated_data["applicant_experience"]["end_date"],
            'job_title': validated_data["applicant_experience"]["job_title"],
            'company_name': validated_data["applicant_experience"]["company_name"],
            'job_location': validated_data["applicant_experience"]["job_location"],
            'description': validated_data["applicant_experience"]["description"],
        }
        applicant_education = {
            'certification_awarded': validated_data["applicant_education"]["certification_awarded"],
            'education_level': validated_data["applicant_education"]["education_level"],
            'institution_name': validated_data["applicant_education"]["institution_name"],
            'start_date': validated_data["applicant_education"]["start_date"],
            'end_date': validated_data["applicant_education"]["end_date"],
            'grade': validated_data["applicant_education"]["grade"]
        }

        applicant_skill = {
            'applicant': validated_data["applicant_skill"]["applicant"],
            'skill': validated_data["applicant_skill"]["skill"],
            'skill_level': validated_data["applicant_skill"]["skill_level"]
        }
        applicant = Applicant.objects.get(user=validated_data["applicant_skill"]["applicant"])
        applicant_education['applicant'] = applicant
        applicant_experience['applicant'] = applicant

        job_application = JobApplication.objects.create(jobpost=validated_data["jobpost"],
                                      applicant=applicant)
        applicant_skill_= ApplicantSkill.objects.create(**applicant_skill)
        applciant_education_ = ApplicantEducation.objects.create(**applicant_education)
        applicant_experience_ = ApplicantExperience.objects.create(**applicant_experience)

        return job_application






