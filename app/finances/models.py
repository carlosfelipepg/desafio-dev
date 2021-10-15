from django.db import models


class TFinances(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    type = models.IntegerField()
    desc_type = models.CharField(blank=True, null=True, max_length=150)
    date_hour = models.DateTimeField(blank=True, null=True)
    value = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=15)
    cpf = models.CharField(blank=True, null=True, max_length=11)
    card = models.CharField(blank=True, null=True, max_length=12)
    store_owner = models.CharField(blank=True, null=True, max_length=14)
    store = models.CharField(blank=True, null=True, max_length=19)

    class Meta:
        managed = True
        db_table = 't_finances'
