from django.shortcuts import render, redirect
from django.http import HttpResponse
import urllib.request
import json
from django.contrib import messages
from .models import Contact
# Create your views here.


def home(request):
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact-us.html')


def weather(request):
    if request.method == "GET":
        city = request.GET.get('city')
        url = "https://api.weatherapi.com/v1/current.json?key=acef0c719e4b4c388fd45825230103&q="+city+"&aqi=yes"
        try:
            source = urllib.request.urlopen(url).read()
        # converting json data to dictionary
            weather_data = json.loads(source)
            print(weather_data.keys())

            data = {
                "country": weather_data["location"]["country"],
                "city": weather_data["location"]["name"],
                "state": weather_data["location"]["region"],
                "localtime": weather_data["location"]["localtime"].split(" ")[1],
                "temp": weather_data["current"]["temp_c"],
                "pressure": weather_data["current"]["pressure_in"],
                "humidity": weather_data["current"]["humidity"],
                "windSpeed": weather_data["current"]["wind_kph"],
                "currentConditon": weather_data["current"]["condition"]["text"],
                "icon": weather_data["current"]["condition"]["icon"],
                "uv": weather_data["current"]["uv"],
            }
            return render(request, 'weather.html', {"data": data})
        except:
            return render(request, 'error.html')
    return redirect('/')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name, email=email, phone=phone, content=content)
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(
                request, "Your message has been successfully sent")

    return render(request, 'contact.html')
