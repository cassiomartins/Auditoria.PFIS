from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditorias', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respostaitem',
            name='evidencia',
        ),
        migrations.AddField(
            model_name='respostaitem',
            name='evidencia_bytes',
            field=models.BinaryField(blank=True, editable=False, null=True, verbose_name='Evidência (bytes)'),
        ),
        migrations.AddField(
            model_name='respostaitem',
            name='evidencia_content_type',
            field=models.CharField(blank=True, max_length=100, verbose_name='MIME type'),
        ),
        migrations.AddField(
            model_name='respostaitem',
            name='evidencia_filename',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nome do arquivo'),
        ),
    ]
