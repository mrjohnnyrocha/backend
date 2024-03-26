from rest_framework.views import APIView
from django.shortcuts import render

class PrivacyPolicyAPI(APIView):
    def get(self, request):
        return render(request, "privacy_policy.html")
