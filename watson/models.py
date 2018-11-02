import collections
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey

from watson.integration import WatsonRequestManager


class WatsonAnalysisResults(models.Model):
    """A set of successfully retrieved & extracted getTone results"""
    # Storing the full response and an abbreviated subset of results
    watson_json = models.TextField()
    # Individual tone scores
    anger = models.DecimalField(max_digits=8, decimal_places=7)
    disgust = models.DecimalField(max_digits=8, decimal_places=7)
    fear = models.DecimalField(max_digits=8, decimal_places=7)
    joy = models.DecimalField(max_digits=8, decimal_places=7)
    sadness = models.DecimalField(max_digits=8, decimal_places=7)
    # Results are linked to the analysed object via a job definition
    job = models.OneToOneField("watson.WatsonAnalysisJob", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Watson analysis results" # Killing the double s in resultss

    def get_primary_emotion(self):
        emotion_fields = ("joy", "fear", "disgust", "anger", "sadness")
        emotion_value_pairs = [{"field": field, "value": getattr(self, field)} for field in emotion_fields]

        emotion_value_pairs = sorted(emotion_value_pairs, key=lambda k: k["value"], reverse=True)

        return emotion_value_pairs[0]["field"]

    def __str__(self):
        return "{job_str} - result: {primary_emotion}"\
            .format(job_str=str(self.job), primary_emotion=self.get_primary_emotion())


class WatsonAnalysisJob(models.Model):
    """An instance of an analysis attempt - distinct from results to keep a record of failures"""
    # In theory we might chose to apply this analysis to any model - so we use a generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_record = GenericForeignKey('content_type', 'object_id')
    # We might also choose to analyse any field
    field_name = models.CharField(max_length=64)

    def get_string(self):
        return getattr(self.related_record, self.field_name)

    def perform_analysis(self):
        watson = WatsonRequestManager()
        results = watson.analyse_tone(self.get_string())
        results.job = self
        results.save()

    def __str__(self):
        return "Analysis on {content_type}:{field_name}"\
            .format(content_type=self.content_type, field_name=self.field_name)


class WatsonAnalysisBase(models.Model):
    """Base mixin model for Watson integration"""
    watson_fields = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        if not isinstance(self.watson_fields, collections.Iterable):
            raise Exception("Configuration Error - please provide 'watson_fields' as an iterable")
        super(WatsonAnalysisBase, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        super(WatsonAnalysisBase, self).save(**kwargs)

        # Here we loop through the observed fields for this model and create jobs for each of them
        job_kwargs = {
            'content_type': ContentType.objects.get_for_model(self),
            'object_id': self.id
        }

        for field_name in self.watson_fields:
            job_kwargs['field_name'] = field_name
            job = WatsonAnalysisJob.objects.create(**job_kwargs)

            if settings.WATSON_ANALYSIS_ASYNC:
                # In reality this is the much more sensible route - no-one wants third party API calls on request thread
                # Architecture builds towards simplicity here even though it won't be implemented
                # Assuming we're using celery the call would look something like:
                # tasks.execute_job.apply_async(job.id)
                pass
            else:
                job.perform_analysis()
