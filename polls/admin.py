from django.contrib import admin

from .models import Question, Choice, Survey, Questionnare, Remark

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Survey)
admin.site.register(Questionnare)
admin.site.register(Remark)