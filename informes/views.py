from django.shortcuts import render

# Create your views here.
def informes(request):
    return render(request, 'informes.html')