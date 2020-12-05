from django.shortcuts import render
from django.http import HttpResponse
from django import forms

class InputForm(forms.Form):
    search = forms.CharField(label="Select City", max_length=50)


def homepage(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
        search = request.GET.get('search')
        print ("*"*100)
        print (form.cleaned_data['search'])
        print ("*"*100)
    else:
        form = InputForm()
    return render(request, 'cityweather/homepage.html', {'form': form})
