# Generated by Django 3.1.1 on 2021-01-11 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_profile', '0002_auto_20210111_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapstudentprofile',
            name='Informational_Text_Key_Ideas_and_Details_STANDARD_ERROR',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='mapstudentprofile',
            name='Informational_Text_Language_Craft_and_Structure_STANDARD_ERROR',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='mapstudentprofile',
            name='Literary_Text_Key_Ideas_and_Details_STANDARD_ERROR',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='mapstudentprofile',
            name='Literary_Text_Language_Craft_and_Structure_STANDARD_ERROR',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='mapstudentprofile',
            name='Vocabulary_Acquisition_and_Use_STANDARD_ERROR',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
