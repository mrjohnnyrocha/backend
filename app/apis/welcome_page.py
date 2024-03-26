from rest_framework.views import APIView
from django.shortcuts import render

class WelcomePageAPI(APIView):
    def get(self, request):
        return render(request, "welcome_page.html")
