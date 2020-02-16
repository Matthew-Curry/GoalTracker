from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
#imports for the dummy view
#NOT SURE IF KEEPING/IF TEMPLATE VIEW IS STILL RELEVANT


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#view for the main SPA app (I think)
class IndexTemplateView(LoginRequiredMixin, TemplateView):
    #settings
    def get_template_names(self):
        template_name = "home.html"
        return template_name

#a dummy view to throw a 400 after api usage
@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)