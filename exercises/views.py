from django.http import HttpResponse


def get_exercise(request, slug: str):
    return HttpResponse('Good luck!')
