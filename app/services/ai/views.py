from django.views import View
from inertia import render


class AIAssistantView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'AIAssistant/HomePage',
            props={}
        )