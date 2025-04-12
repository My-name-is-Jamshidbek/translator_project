from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Translation

def index(request):
    """Bosh sahifani render qiladi."""
    return render(request, "index.html")

def ajax_translate(request):
    """
    AJAX POST so'rovlarini qabul qilib, tarjimani qidiradi.
    Kiritilgan so'z va tarjima yo'nalishiga asoslangan holda qidiruv bajariladi va
    natija sifatida tarjima so'zi bilan birga tavsif (description) ham qaytariladi.
    """
    if request.method == "POST":
        input_text = request.POST.get("text", "").strip()
        direction = request.POST.get("direction", "uz_to_kh").strip().lower()

        if not input_text:
            return JsonResponse({"error": "Matn kiritilmagan."}, status=400)

        record = None
        if direction == "uz_to_kh":
            qs = Translation.objects.filter(
                Q(uz_word__iexact=input_text) | Q(uz_word__icontains=input_text)
            )
            if qs.exists():
                record = qs.first()
                translation = record.kh_word
            else:
                translation = "Tarjima topilmadi"
        elif direction == "kh_to_uz":
            qs = Translation.objects.filter(
                Q(kh_word__iexact=input_text) | Q(kh_word__icontains=input_text)
            )
            if qs.exists():
                record = qs.first()
                translation = record.uz_word
            else:
                translation = "Tarjima topilmadi"
        else:
            return JsonResponse({"error": "Noto'g'ri yo'nalish."}, status=400)

        description = record.description if record and record.description else ""
        return JsonResponse({"translation": translation, "description": description})
    else:
        return JsonResponse({"error": "So'rov metodi noto'g'ri."}, status=400)

def ajax_suggestions(request):
    """
    GET so'rovlari orqali dinamik tavsif va so'z takliflarini qaytaradi.
    Parametr sifatida 'q' (qidiruv so'zi) va 'direction' (tarjima yo'nalishi) qabul qilinadi.
    """
    query = request.GET.get("q", "").strip().lower()
    direction = request.GET.get("direction", "uz_to_kh").strip().lower()

    if direction == "kh_to_uz":
        suggestions_qs = Translation.objects.filter(kh_word__icontains=query)
    else:
        suggestions_qs = Translation.objects.filter(uz_word__icontains=query)

    # Qidiruv bo'sh bo'lsa, dastlabki 10 ta yozuvni qaytaramiz.
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
