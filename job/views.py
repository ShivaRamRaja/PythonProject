from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import JobPost, Applicant
from .serializers import LoginSerializer, JobApplication, \
    JobPostSerializer, JobApplicationSerializer, ApplicantSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
#import boto3
from botocore.exceptions import ClientError
import os
import random
import json
import boto3
from botocore.config import Config

# Create your views here.

class HomeAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'homepage.html'
    http_method_names = ['get']

    def get(self, request):

        return Response({},template_name='homepage.html')


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_login.html'
    serializer_class = LoginSerializer
    http_method_names = ['get', 'post']

    def get(self, request):
        serializer = self.serializer_class()
        return Response({'serializer': serializer})

    def post(self, request):
        # user = {'email': request.data['email'], 'password': request.data['password']}
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        
        #Sending the New SignUp mail using lambda Service
        lambdafunctionname = "JobPortal"
        config = Config(read_timeout=5000,
                        connect_timeout=300,
                        retries={"max_attempts": 4})
        lambdafuninput =  {}
        session = boto3.Session()
        lambda_client = session.client('lambda', config=config, region_name='us-east-1')
        response = lambda_client.invoke(FunctionName=lambdafunctionname,
                                    InvocationType='RequestResponse',
                                    Payload=json.dumps(lambdafuninput))
        res_str = response['Payload'].read()
        
        '''
        #Lambda block for triggeriing publishing sns message
        lambdafunctionname = "snstrigger"
        config = Config(read_timeout=5000,
                        connect_timeout=300,
                        retries={"max_attempts": 4})
        lambdafuninput =  {}
        session = boto3.Session()
        lambda_client = session.client('lambda', config=config, region_name='us-east-1')
        response = lambda_client.invoke(FunctionName=lambdafunctionname,
                                    InvocationType='RequestResponse',
                                    Payload=json.dumps(lambdafuninput))
        res_str = response['Payload'].read()
        '''
        
        
                
        '''
        print("Login Notification")
        topic_arn = 'arn:aws:sns:us-east-1:365388303609:jobportalSNS'
        message = 'You Have Been Successfully Logged Into Your Job Portal, All The Best On Finding Your Dream Job.'
        subject = 'Loggin Notification Message For User.'
        AWS_REGION = 'us-east-1'
        sns_client = boto3.client('sns', region_name=AWS_REGION)
        response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject,
        )['MessageId']  
        '''
        
        return redirect('job_post')


class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_logout.html'

    def get(self, request):
        return redirect('user_login') 
        

class ApplicantView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration.html'
    serializer_class = ApplicantSerializer
    http_method_names = ['get', 'post']

    def get(self, request):
        serializer = self.serializer_class()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('user_login')


class JobPostTemplateHTMLRender(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        data = super().get_template_context(data, renderer_context)
        if not data:
            return {}
        else:
            return data


class JobPostAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'jobs_list.html'
    serializer_class = JobPostSerializer
    queryset = JobPost.objects.all()
    lookup_field = ["id"]

    def get(self, request):
        queryset = JobPost.objects.all()
        return Response({'jobpost': queryset})


class JobPostAPIViewOne(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'jobs_list.html'
    serializer_class = JobPostSerializer
    queryset = JobPost.objects.all()

    def get(self, request, id=None):
        queryset = JobPost.objects.get(id=id)
        return redirect('job_application')


class JobApplicationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'job_application.html'
    serializer_class = JobApplicationSerializer
    http_method_names = ['get', 'post']

    def get(self, request, id=None, *args , **kwargs):
        global value
        if id:
            value=id
        serializer = self.serializer_class()
        return Response({'serializer': serializer})

    def post(self, request, *args, **kwargs):
        application = request.data.copy()
        application['jobpost'] = value
        serializer = self.serializer_class(data=application)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('job_applications')


class JobApplicationsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'applications.html'
    serializer_class = JobApplicationSerializer
    http_method_names = ['get']

    def get(self, request):
        try:
            applicant = Applicant.objects.get(user=self.request.user)
        except Applicant.DoesNotExist:
            applicant=None
        queryset = JobApplication.objects.filter(applicant=applicant)
        return Response({'jobapplications': queryset})
