from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        roll = request.POST.get('roll')
        print(name, phone, roll)
    return render(request, 'index.html')
