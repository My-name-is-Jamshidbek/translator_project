# translator_app/views.py

import re

from django.db.models.expressions import result
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from .gap import uz_to_kh_sentence
from .models import Translation
import pandas as pd
import os

# XLSX faylini o'qish
df = pd.read_excel('translator_app/umumiy.xlsx')  # Fayl nomini o'zingiznikiga moslashtiring

def uz_to_kh(word, df=df):
    # Adabiy so'z (B ustuni) bo'yicha qidirish
    result = df[df['B'].str.lower() == word.lower()]
    if not result.empty:
        res = ""
        for _, row in result.iterrows():
            res += f"{word.lower()} - {row['A'].lower()} - {row['C']}<br>"
    else:
        return f"{word.lower()} (hozircha bazada mavjud emas)"
    return res

def kh_to_uz(word, df=df):
    # Sheva so'z (A ustuni) bo'yicha qidirish
    result = df[df['A'].str.lower() == word.lower()]
    if not result.empty:
        res = ""
        for _, row in result.iterrows():
            res += f"{word.lower()} - {row['B'].lower()} - {row['C']}<br>"
    else:
        return f"{word.lower()} (hozircha bazada mavjud emas)"
    return res

def index(request):
    """Bosh sahifani render qiladi."""
    result = ""
    sentence = None
    direction = None
    if request.method == "POST":
        sentence = request.POST['sentence']
        direction = request.POST['direction']
        if len(sentence.split(" ")) > 1:
            if direction == "uz_to_kh":
                result = uz_to_kh_sentence(sentence)
            else:
                result = "Xozircha mavjud emas"
        else:
            if direction == "uz_to_kh":
                result = uz_to_kh(sentence)
            else:
                result = kh_to_uz(sentence)
    return render(request, "index.html", context={"result": result, "sentence": sentence, "direction": direction})

