# Generated by Django 2.1.3 on 2018-11-01 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatsonAnalysisJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('field_name', models.CharField(max_length=64)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='WatsonAnalysisResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watson_json', models.TextField()),
                ('anger', models.DecimalField(decimal_places=7, max_digits=8)),
                ('disgust', models.DecimalField(decimal_places=7, max_digits=8)),
                ('fear', models.DecimalField(decimal_places=7, max_digits=8)),
                ('joy', models.DecimalField(decimal_places=7, max_digits=8)),
                ('sadness', models.DecimalField(decimal_places=7, max_digits=8)),
                ('job', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='watson.WatsonAnalysisJob')),
            ],
        ),
    ]
