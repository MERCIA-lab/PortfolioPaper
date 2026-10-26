from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_portfolio_github_portfolio_github_summary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='location',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
