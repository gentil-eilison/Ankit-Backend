# Generated by Django 4.2.11 on 2024-04-07 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("study_sessions", "0004_alter_historicalstudysession_cards_added_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalstudysession",
            old_name="spreadsheet_file",
            new_name="csv_file",
        ),
        migrations.RenameField(
            model_name="studysession",
            old_name="spreadsheet_file",
            new_name="csv_file",
        ),
    ]
