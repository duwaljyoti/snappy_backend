from django.db import models


class LoadTestRecord(models.Model):
    """Throwaway rows for database load tests. See the db-* views."""
    name = models.CharField(max_length=100)
    payload = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
