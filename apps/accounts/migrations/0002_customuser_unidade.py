import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('auditorias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='unidade',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='usuarios',
                to='auditorias.unidade',
                verbose_name='Unidade',
            ),
        ),
    ]
