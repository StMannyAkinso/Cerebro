from django.db import models


class Account(models.Model):
    ACCOUNT_TYPES = [
        ("current", "Current Account"),
        ("savings", "Savings Account"),
        ("investment", "Investment Account"),
        ("credit_card", "Credit Card"),
        ("cash", "Cash"),
        ("business", "Business Account"),
    ]

    name = models.CharField(
        max_length=100,
    )

    provider = models.CharField(
        max_length=100,
        blank=True,
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
    )

    currency = models.CharField(
        max_length=3,
        default="GBP",
    )

    is_active = models.BooleanField(
        default=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name