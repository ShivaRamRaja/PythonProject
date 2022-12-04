from datetime import datetime
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from model_utils import Choices

from common.models import AbstractBase
from company.models import Company


# Create your models here.
class Applicant(AbstractBase):
    """A model to store the details of the jobapplicant. """
    user = models.ForeignKey(User, related_name='applicant', on_delete=models.CASCADE)
    firstname = models.CharField(null=True, blank=True, max_length=50)
    secondname = models.CharField(null=True, blank=True, max_length=50)
    email = models.CharField(max_length=30, unique=True)
    relocation = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.firstname + self.secondname

    class Meta:
        verbose_name= 'applicant'
        verbose_name_plural='applicants'
        ordering = ("created_at", "-updated_at")
        db_table = 'applicant'


class ApplicantExperience(AbstractBase):
    """A model to store the experience details of the jobapplicant."""
    applicant = models.ForeignKey(Applicant, related_name='applicant_experience', on_delete=models.CASCADE)
    is_current = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    job_title = models.CharField(null=True, blank=True, max_length=50)
    company_name = models.CharField(null=True, blank=True, max_length=50)
    job_location = models.CharField(null=True, blank=True, max_length=50)
    description = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self) -> str:
        return self.job_title + self.company_name

    class Meta:
        verbose_name = 'applicant_experience'
        verbose_name_plural = 'applicants_experience'
        ordering = ("created_at", "-updated_at")
        db_table = 'applicantexperience'


class ApplicantEducation(AbstractBase):
    """A model to store the education level of a jobapplicant."""
    EDU_LEVEL_CHOICES = Choices(
        ("primary", _("Primary")),
        ("highschool", _("High School")),
        ("undergraduate", _("Undergraduate")),
        ("tertiary", _("Tertiary")),
        ("other", _("Other"))
    )
    applicant = models.ForeignKey(Applicant, related_name='applicant_education', on_delete=models.CASCADE)
    certification_awarded = models.CharField(null=True, blank=True, max_length=50)
    education_level = models.CharField(
        _("education level"),
        choices=EDU_LEVEL_CHOICES,
        default="primary",
        max_length=50
    )
    institution_name = models.CharField(null=True, blank=True, max_length=60)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    grade = models.CharField(null=True, blank=True, max_length=10)

    def __str__(self) -> str:
        return self.certification_awarded

    class Meta:
        verbose_name = 'applicant_education'
        verbose_name_plural = 'applicants_education'
        ordering = ("created_at", "-updated_at")
        db_table = 'applicanteducation'


class Skill(AbstractBase):
    """A model to store the skills"""
    name = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'skill'
        verbose_name_plural = 'skills'
        ordering = ("created_at", "-updated_at")
        db_table = 'skill'


class ApplicantSkill(AbstractBase):
    """A model to store the set of skills of a jobapplicant."""
    SKILL_LEVEL_CHOICES = (
        ("beginner", _("Beginner")),
        ("intermediate", _("Intermediate")),
        ("professional", _("Professional"))
    )
    applicant = models.ForeignKey(User, related_name='applicant_skill', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='applicant_skill', on_delete=models.CASCADE)
    skill_level = models.CharField(
        _("skill level"),
        choices = SKILL_LEVEL_CHOICES,
        default="beginner",
        max_length= 30
    )

    def __str__(self) -> str:
        str(self.applicant) + str(self.skill_level)

    class Meta:
        verbose_name = 'applicant_skill'
        verbose_name_plural = 'applicants_skill'
        ordering = ("created_at", "-updated_at")
        db_table = 'applicantskill'


class JobPost(AbstractBase):
    """A model to store a job post."""
    company = models.ForeignKey(Company, related_name="company_post", on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    description = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=50)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self) -> str:
        return self.role

    class Meta:
        verbose_name = 'jobpost'
        verbose_name_plural = 'jobspost'
        ordering = ("created_at", "-updated_at")
        db_table = 'jobpost'


class JobPostSkill(AbstractBase):
    """A model to store the jobpost skillset."""
    SKILL_LEVEL_CHOICES = (
        ("beginner", _("Beginner")),
        ("intermediate", _("Intermediate")),
        ("professional", _("Professional"))
    )
    jobpost = models.ForeignKey(JobPost, related_name="jobpostskillset", on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name="skillset", on_delete=models.CASCADE)
    skill_level = models.CharField(
        _("skill level"),
        choices=SKILL_LEVEL_CHOICES,
        default="beginner",
        max_length=30
    )

    class Meta:
        verbose_name = 'jobpostskill'
        verbose_name_plural = 'jobspostskills'
        ordering = ("created_at", "-updated_at")
        unique_together = ('jobpost', 'skill')
        db_table = 'jobpostskill'


class JobApplication(AbstractBase):
    """A model to store the job applications"""
    STATUS_CHOICES = (
        ("new", _("New")),
        ("under_review", _("Under_Review")),
        ("accepted", _("Accepted")),
        ("rejected", _("Rejected"))
    )
    applicant = models.ForeignKey(Applicant, related_name="applicantapplication", on_delete=models.CASCADE)
    jobpost = models.ForeignKey(JobPost, related_name="jobpostapplication", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(
        _("application status"),
        choices=STATUS_CHOICES,
        default="new",
        max_length=30
    )

    def __str__(self) -> str:
        return self.applicant.firstname + self.status

    class Meta:
        verbose_name = 'jobapplication'
        verbose_name_plural = 'jobapplications'
        ordering = ("created_at", "-updated_at")
        db_table = 'jobapplication'


@receiver(post_save, sender=JobApplication)
def send_notification_on_job_application(sender, instance, created, **kwargs):
    """A post  save signal to send an email once a job application has been created. """

    #New order has been created.
    if created:
        message = f'We have received your application for {instance.jobpost.role}. Thank you. All the best'
        send_mail(
            'New Job Application',
            message,
            'xyz@gmail.com',
            [instance.applicant.user.email]
        )

    else:
        if instance.status == 'accepted' or instance.status == 'rejected':
            message = f'Your job application has been updated'
            send_mail(
                'Job Application Updated',
                message,
                'xyz@gmail.com',
                [instance.applicant.user.email]
            )

