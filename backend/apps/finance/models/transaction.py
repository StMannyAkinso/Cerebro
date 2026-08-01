from django.db import models

from .account import Account


class Transaction(models.Model):
    SOURCE_TYPES = [
        ("manual", "Manual"),
        ("csv_import", "CSV Import"),
        ("bank_import", "Bank Import"),
        ("api_import", "API Import"),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    transaction_date = models.DateField()

    description = models.CharField(
        max_length=255,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Positive for income, negative for expenses",
    )

    balance_after = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    reference = models.CharField(
        max_length=255,
        blank=True,
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        default="manual",
    )

    imported_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-transaction_date", "-id"]

    def __str__(self):
        return (
            f"{self.transaction_date} | "
            f"{self.description} | "
            f"{self.amount}"
        )