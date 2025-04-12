from django.db import models

class Translation(models.Model):
    uz_word = models.CharField(max_length=200, help_text="The word in Uzbek")
    kh_word = models.CharField(max_length=200, help_text="The translation in Khorezm")

    def __str__(self):
        return f"{self.uz_word} - {self.kh_word}"
