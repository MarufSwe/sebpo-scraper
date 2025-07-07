from django.db import models

class ScrapedItem(models.Model):
    name = models.CharField(max_length=255, unique=True)

    finding_date = models.DateField(null=True, blank=True)
    finding_url = models.URLField(null=True, blank=True)

    nprm_date = models.DateField(null=True, blank=True)
    nprm_url = models.URLField(null=True, blank=True)

    final_rule_date = models.DateField(null=True, blank=True)
    final_rule_url = models.URLField(null=True, blank=True)

    rescinded_date = models.DateField(null=True, blank=True)
    rescinded_url = models.URLField(null=True, blank=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
