# translator_app/views.py

import re
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Translation


def index(request):
    """Bosh sahifani render qiladi."""
    return render(request, "index.html")


def translate_sentence(text, direction="uz_to_kh"):
    """
    Kiritilgan gap yoki iborani so‘zma-so‘z tarjima qiladi.
    Har bir so‘z uchun agar bazada mos yozuv aniqlanmasa,
    u so‘z "(Kiritilmagan)" qo'shimchasi bilan ko'rsatiladi.

    Agar tarjima yozuvi mavjud bo'lsa va tavsif mavjud bo'lsa,
    natijada "tarjima (tavsif)" shaklida ko‘rsatiladi.
    """
    # So'zlar va punktuatsiyani aniqlash (qat'iy so'zlar va maxsus belgilarni ajratib olish)
    tokens = re.findall(r"[\w']+|[.,!?;]", text)
    translated_tokens = []

    for token in tokens:
        if token.isalpha():
            if direction == "uz_to_kh":
                qs = Translation.objects.filter(uz_word__iexact=token)
            else:  # "kh_to_uz"
                qs = Translation.objects.filter(kh_word__iexact=token)

            if qs.exists():
                translation_obj = qs.first()
                if direction == "uz_to_kh":
                    translation = translation_obj.kh_word
                else:
                    translation = translation_obj.uz_word
                desc = translation_obj.description.strip() if translation_obj.description else ""
                if desc:
                    translated_tokens.append(f"{translation} ({desc})")
                else:
                    translated_tokens.append(translation)
            else:
                # Agar so‘z topilmasa, qo‘shamiz: so‘z (Kiritilmagan)
                translated_tokens.append(f"{token} (Kiritilmagan)")
        else:
            # Punktuatsiya yoki raqamlar o'z holicha
            translated_tokens.append(token)

    # Natijaviy gapni yig'ish – punktuatsiya oldidan bo'shliqni to'g'ri qo‘llash
    result = ""
    for t in translated_tokens:
        if t in ".,!?;":
            result = result.rstrip() + t + " "
        else:
            result += t + " "
    return result.strip()


def ajax_translate(request):
    """
    AJAX POST so'rovlari orqali gap tarjimasini amalga oshiradi.
    So'rovda:
      - text: Tarjima qilinadigan gap yoki ibora.
      - direction: "uz_to_kh" (O'zbek → Xorazm) yoki "kh_to_uz" (Xorazm → O'zbek).
    Natija JSON formatida qaytariladi.
    """
    if request.method == "POST":
        input_text = request.POST.get("text", "").strip()
        direction = request.POST.get("direction", "uz_to_kh").strip().lower()

        if not input_text:
            return JsonResponse({"error": "Matn kiritilmagan."}, status=400)

        translation = translate_sentence(input_text, direction)
        return JsonResponse({"translation": translation})
    else:
        return JsonResponse({"error": "So'rov metodi noto'g'ri."}, status=400)


def ajax_suggestions(request):
    """
    GET so'rovlari orqali dinamik taklif va tavsif ma'lumotlarini qaytaradi.

    Parametrlar:
      - q: Qidiruv matni.
      - direction: "uz_to_kh" yoki "kh_to_uz".
    """
    query = request.GET.get("q", "").strip().lower()
    direction = request.GET.get("direction", "uz_to_kh").strip().lower()

    if direction == "kh_to_uz":
        suggestions_qs = Translation.objects.filter(kh_word__icontains=query)
    else:
        suggestions_qs = Translation.objects.filter(uz_word__icontains=query)

    if not query:
        suggestions_qs = suggestions_qs[:10]

    suggestions_list = [
        {
            "uz": t.uz_word,
            "kh": t.kh_word,
            "description": t.description
        }
        for t in suggestions_qs
    ]
    return JsonResponse({"suggestions": suggestions_list})
