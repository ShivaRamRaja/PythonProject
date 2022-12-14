from django.contrib import admin
from .models import \
    Applicant, ApplicantExperience, \
    ApplicantSkill, ApplicantEducation, \
    Skill, JobPost, JobApplication


# Register your models here.

class ApplicantAdmin(admin.ModelAdmin):

    list_filter = ('email',)


class ApplicantExperienceAdmin(admin.ModelAdmin):

    list_filter = ('company_name',)

admin.site.register(ApplicantSkill)
admin.site.register(Skill)
admin.site.register(ApplicantEducation)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(ApplicantExperience, ApplicantExperienceAdmin)
admin.site.register(JobPost)
admin.site.register(JobApplication)