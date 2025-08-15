from django.db import models


class BalanceArticle(models.Model):
    """Статья баланса"""

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Статья баланса"
        verbose_name_plural = "Статьи баланса"

    def __str__(self) -> str:
        return self.name


class BalanceGroup(models.Model):
    """Балансовая группа"""

    article = models.ForeignKey(
        BalanceArticle, on_delete=models.PROTECT, related_name="groups"
    )
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("article", "name")
        verbose_name = "Балансовая группа"
        verbose_name_plural = "Балансовые группы"

    def __str__(self) -> str:
        return f"{self.article} / {self.name}"
