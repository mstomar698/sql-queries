from django.shortcuts import render

# Create your views here.


def table(request):
    return render(request, 'table/table.html')


def certificates(request):
    return render(request, 'table/certificates.html')
