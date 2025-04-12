from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Translation


def index(request):
    """Render the main translator page."""
    return render(request, "index.html")


def ajax_translate(request):
    """
    Handle AJAX POST requests for translation.

    Expects POST data containing:
      - 'text': The word or phrase to translate.
      - 'direction': "uz_to_kh" (Uzbek to Khorezm) or "kh_to_uz" (Khorezm to Uzbek).

    Returns a JSON response with the translation.
    """
    if request.method == "POST":
        input_text = request.POST.get("text", "").strip()
        direction = request.POST.get("direction", "uz_to_kh").strip().lower()

        if not input_text:
            return JsonResponse({"error": "No input text provided."}, status=400)

        if direction == "uz_to_kh":
            qs = Translation.objects.filter(
                Q(uz_word__iexact=input_text) | Q(uz_word__icontains=input_text)
            )
            translation = qs.first().kh_word if qs.exists() else "Translation not found"
        elif direction == "kh_to_uz":
            qs = Translation.objects.filter(
                Q(kh_word__iexact=input_text) | Q(kh_word__icontains=input_text)
            )
            translation = qs.first().uz_word if qs.exists() else "Translation not found"
        else:
            return JsonResponse({"error": "Invalid translation direction."}, status=400)

        return JsonResponse({"translation": translation})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)


def ajax_suggestions(request):
    """
    Returns dynamic suggestions from the Translations table.

    Accepts GET parameters:
      - 'q': The query string.
      - 'direction': "uz_to_kh" or "kh_to_uz" to determine which field to search.
    """
    query = request.GET.get("q", "").strip().lower()
    direction = request.GET.get("direction", "uz_to_kh").strip().lower()

    # If direction is kh_to_uz, search in the kh_word column; otherwise in uz_word.
    if direction == "kh_to_uz":
        suggestions_qs = Translation.objects.filter(kh_word__icontains=query)
    else:
        suggestions_qs = Translation.objects.filter(uz_word__icontains=query)

    # Limit to the first 10 suggestions if query is empty or too many results are returned
    if not query:
        suggestions_qs = suggestions_qs[:10]

    suggestions_list = [{"uz": t.uz_word, "kh": t.kh_word} for t in suggestions_qs]
    return JsonResponse({"suggestions": suggestions_list})
