from django.contrib import admin

from watson.models import WatsonAnalysisJob, WatsonAnalysisResults

admin.site.register(WatsonAnalysisJob)
admin.site.register(WatsonAnalysisResults)
