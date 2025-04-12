from django.db import models

class Translation(models.Model):
    uz_word = models.CharField(max_length=200, help_text="O'zbek so'zi")
    kh_word = models.CharField(max_length=200, help_text="Xorazm tarjimasi")
    description = models.CharField(
        max_length=250,
        blank=True,
        default="Bogotdo ishlatiladi",
        help_text="So'z ma'nosi, izohi yoki qo'shimcha ma'lumot"
    )

    def __str__(self):
        return f"{self.uz_word} – {self.kh_word}"
