from django.db import models
from django.contrib.auth.models import User


class BenchmarkModel(models.Model):
    MODEL_STATUS = (
        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED"),
        ("REJECTED", "REJECTED"),
    )
    model_mlcube = models.ForeignKey("mlcube.MlCube", on_delete=models.PROTECT)
    benchmark = models.ForeignKey("benchmark.Benchmark", on_delete=models.CASCADE)
    initiated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    metadata = models.JSONField()
    approval_status = models.CharField(
        choices=MODEL_STATUS, max_length=100, default="PENDING"
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ["-priority"]
