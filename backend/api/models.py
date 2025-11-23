from django.db import models

class EquipmentDataset(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)

    # Min-Max
    min_flowrate = models.IntegerField(default=0)
    min_pressure = models.FloatField(default=0.0)
    min_temperature = models.FloatField(default=0.0)

    max_flowrate = models.IntegerField(default=0)
    max_pressure = models.FloatField(default=0.0)
    max_temperature = models.FloatField(default=0.0)

    type_distribution = models.JSONField(default=dict)

    rows = models.JSONField(default=list)

    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at}"
