from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from . models import *
# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login', messages)
    else:
        return render(request, 'login/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        location = request.POST['location']
        phone = request.POST['phone']
        email_address = request.POST['email_address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email_address).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email_address, first_name=first_name, last_name=last_name, is_staff=False)
                user.save();
                client = Client.objects.create(user=user, location=location, phone=phone)
                client.save();
                return render('/')
    else:
        return render(request, 'login/register.html')

def treatment(request):
    if request.method == 'POST':
        name = request.POST['name']
        cost = request.POST['cost']

        treat = Treatment.objects.create(name=name, cost=cost)
        treat.save();

    else:
        treats = Treatment.objects.all()
        context = {'treats': treats, 'user': user}
        return render(request, 'login/login.html', context)

def animalReg(request):
    if request.method == 'POST':
        breed = request.POST['breed']
        years = request.POST['years']
        sex = request.POST['sex']
        weight = request.POST['weight']



        animal = Animal.objects.create(user=user, breed=breed, years=years, sex=sex, weight=weight)
        animal.save();
        user.save();

    else:
        animal = Animal.objects.all(user=user)
        animal = {'treats': treats, 'user': user}
        return render(request, 'login/login.html', context)

def animalRegAdmin(request):
    if request.method == 'POST':
        breed = request.POST['breed']
        years = request.POST['years']
        sex = request.POST['sex']
        weight = request.POST['weight']
        user = request.POST['user']

        if request.POST['diseases']:
            diseases = request.POST['diseases']:
        if request.POST['treatment']:
            treat = request.POST['treatment']:
        if request.POST['recommendations']:
            recomend = request.POST['recommendations']:

        user = User.objects.get_or_create(username=user)



        animal = Animal.objects.update_or_create(breed=breed, years=years, sex=sex, weight=weight, diseases=diseases, treatment=treatment, recomend=recommendations, user=user.id)
        animal.save();
        user.save();

    else:
        animal = Animal.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'login/login.html', context)

def appointment(request):
    if request.method == 'POST':
        message = request.POST['message']
        animal = request.POST['animal']
        date =  request.POST['date']   



        book = Appointment.objects.create(message=message, animal=animal, date=date, user=user)
        animal.save();
        user.save();

    else:
        animal = Appointment.objects.all(user=user)
        animal = {'treats': treats, 'user': user}
        return render(request, 'login/login.html', context)

def appointmentAdmin(request):
    if request.method == 'POST':
        tag = request.POST['id']

        if Appointment.objects.get_or_create(animal=tag):
            status = request.POST['status']
            book = Appointment.objects.update_or_create(animal=tag, status=status)
            book.save()

    else:
        animal = Appointment.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'login/login.html', context)

def sales(request):
    if request.method == 'POST':
        user = request.POST['user']
        treatment = request.POST['treatment']  

        sale = Sales.objects.create(user=user, treatment=treatment)
        sale.save();

    else:
        animal = Sales.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'login/login.html', context)

def salesAdmin(request):
    if request.method == 'POST':
        user = request.POST['user']
        treatment = request.POST['treatment']  
        status = request.POST['status']  

        sale = Sales.objects.create(user=user, treatment=treatment, status=status)
        sale.save();

    else:
        animal = Sales.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'login/login.html', context)

    
