
from django.contrib.auth.models import User, auth
from django.contrib import messages
import pandas as pd
import csv
import os
import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
import home.models as homeling
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as Client1
import requests
import json
from django.templatetags.static import static
import base64
from heyoo import WhatsApp
# Create your views here.

messenger = WhatsApp('EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD',  phone_number_id='109461665230077')

VERIFY_TOKEN = "23189345712"

head = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'}


def home(request):
    clients = Client.objects.all()
    for cli in clients:
        if Animal.objects.all().filter(user=cli.user):
            Animal.objects.all().filter(user=cli.user).update(book=cli.book)





    return render(request, 'Medilab/index.html')

def admin(request):
    return redirect('admin/')

def animal_reg(request):
    return render(request, 'Medilab/logs/animal_reg.html')

def logout(request):
	
	auth.logout(request)
	
	return redirect('login')

def appointment_reg(request):
    user = request.user
    animals = Animal.objects.all().filter(user=user)
    context = {'animals': animals, 'user': user}
    return render(request, 'Medilab/logs/appointments.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
           
                auth.login(request, user)
                return redirect('animalReg')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'Medilab/pages-login.html')


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
                return redirect('login')
    else:
        return render(request, 'Medilab/pages-register.html')

def treatment(request):
    if request.method == 'POST':
        name = request.POST['name']
        cost = request.POST['cost']

        treat = Treatment.objects.create(name=name, cost=cost)
        treat.save();

    else:
        treats = Treatment.objects.all().filter(user=request.user)
        context = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/treatmentsReg.html', context)

def animalReport(request):
    brahman = Animal.objects.all().filter(breed="Brahman")
    brahmancount = 0
    for i in brahman:
        brahmancount = brahmancount + 1

    fries = Animal.objects.all().filter(breed="Friesland Holstein")
    friescount = 0
    for i in fries:
        friescount = friescount + 1

    beef = Animal.objects.all().filter(breed="Beef Cattle")
    beefcount = 0
    for i in beef:
        beefcount = beefcount + 2

    context = {'brahmancount': brahmancount, 'friescount': friescount, 'beefcount': beefcount}
    
    return render(request, 'Medilab/logs/animalReport.html', context)

def receipt(request):

    user = request.user

    receipts = Sales.objects.all().filter(user=request.user, paid=True)

    context = {'receipts': receipts, 'user': user}

    return render(request, 'Medilab/logs/salesView.html', context)

def invoice(request):

    if request.method == 'POST':

        saleID = request.POST['saleID']

        sale = Sales.objects.get(id=saleID)

        sale.paid = True

        sale.save()

        user = request.user

        invoices = Sales.objects.all().filter(user=request.user, paid=False)

        messages.info(request, 'Paid Successfully!!!')

        context = {'invoices': invoices, 'user': user}

        return render(request, 'Medilab/logs/invoicesView.html', context)


    user = request.user

    invoices = Sales.objects.all().filter(user=request.user, paid=False)

    context = {'invoices': invoices, 'user': user}

    return render(request, 'Medilab/logs/invoicesView.html', context)


def subscriptionsPay(request):

    user = request.user

    payment_date = datetime.datetime.now()

    expiry_date = payment_date.replace(month = payment_date.month + 1)


    subscrips = Subscriptions.objects.all().filter(user=request.user)

    for subscrip in subscrips:

        check = subscrip.expiry_date.month - payment_date.month

        if check >= 1:

            print(subscrip.expiry_date.month)

            print(payment_date.month)

            messages.info(request, 'Your subscription hasnt expired yet')

            return redirect('subscriptions')




    subs = Subscriptions.objects.create(user=user, payment_date=payment_date, expiry_date=expiry_date)

    subs.save();

    messages.info(request, 'Paid Successfully!!!')

    return redirect('subscriptions')




def subscriptions(request):

    user = request.user

    subs = Subscriptions.objects.all().filter(user=request.user)

    context = {'subs': subs, 'user': user}

    return render(request, 'Medilab/logs/subscriptionsView.html', context)


def animalReg(request):
    if request.method == 'POST':
        breed = request.POST['breed']
        years = request.POST['years']
        sex = request.POST['sex']
        weight = request.POST['weight']

        user = request.user



        animal = Animal.objects.create(user=user, breed=breed, years=years, sex=sex, weight=weight)
        animal.save();
        user.save();
        user = request.user
        animals = Animal.objects.all().filter(user=request.user)
        context = {'animals': animals, 'user': user}
        return render(request, 'Medilab/logs/animalView.html', context)

    else:
            cli = Client.objects.get(user=request.user)
            if cli.clientType == "Farmer":

                user = request.user
                animals = Animal.objects.all().filter(user=request.user)
                context = {'animals': animals, 'user': user}
                return render(request, 'Medilab/logs/animalView.html', context)
            if cli.clientType == "Officer":

                user = request.user
                animals = Animal.objects.all()
                context = {'animals': animals, 'user': user}
                return render(request, 'Medilab/logs/animalViewOfficer.html', context)
            
            if cli.clientType == "Doctor":

                user = request.user
                animals = Animal.objects.all().filter(referred=True)
                context = {'animals': animals, 'user': user}
                return render(request, 'Medilab/logs/animalViewDoctor.html', context)

def animalRegAdmin(request):
    if request.method == 'POST':
        breed = request.POST['breed']
        years = request.POST['years']
        sex = request.POST['sex']
        weight = request.POST['weight']
        user = request.POST['user']

        if request.POST['diseases']:
            diseases = request.POST['diseases']
        if request.POST['treatment']:
            treat = request.POST['treatment']
        if request.POST['recommendations']:
            recomend = request.POST['recommendations']

        user = User.objects.get_or_create(username=user)



        animal = Animal.objects.update_or_create(breed=breed, years=years, sex=sex, weight=weight, diseases=diseases, treatment=treatment, recommendations=recomend, user=user.id)
        animal.save();
        user.save();

    else:
        animal = Animal.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/animal_reg_admin.html', context)

def appointment(request):
    if request.method == 'POST':
        message = request.POST['message']
        animal = request.POST['animal']
        date =  request.POST['date']   

        animal = Animal.objects.get(tag=animal)

        doctor = Doctor.objects.get(speciality=animal.breed)

        doctor = Client.objects.get(user=doctor.user)



        user = request.user
        book = Appointment.objects.create(message=message, animal=animal, date=date, user=user, doctorphone=doctor.phone)
        animal.save();
        user.save();
        user = request.user
        appointments = Appointment.objects.all().filter(user=user)
        context = {'appointments': appointments, 'user': user, 'doctor': doctor}
        return render(request, 'Medilab/logs/appointmentView.html', context)

    else:
            cli = Client.objects.get(user=request.user)
            if cli.clientType == "Farmer":


                user = request.user
                appointments = Appointment.objects.all().filter(user=user)
                context = {'appointments': appointments, 'user': user}
                return render(request, 'Medilab/logs/appointmentView.html', context)
            if cli.clientType == "Officer":

                user = request.user
                appointments = Appointment.objects.all()
                context = {'appointments': appointments, 'user': user}
                return render(request, 'Medilab/logs/appointmentViewAdmin.html', context)
            
            if cli.clientType == "Doctor":

                user = request.user
                appointments = Appointment.objects.all()
                context = {'appointments': appointments, 'user': user}
                return render(request, 'Medilab/logs/appointmentViewAdmin.html', context)

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
        return render(request, 'Medilab/logs/appointments_admin.html', context)

def sales(request):
    if request.method == 'POST':
        user = request.POST['user']
        treatment = request.POST['treatment']  

        sale = Sales.objects.create(user=user, treatment=treatment)
        sale.save();

    else:
        animal = Sales.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/sales.html', context)

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
        return render(request, 'Medilab/logs/sales_admin.html', context)

def prediction(request):
    if request.method == 'POST':
        symptoms = Symptoms.objects.all()
        
        keywords = symptoms
        post_symptoms = []
        for key in symptoms:
            post_symptom = request.POST.get(key.name)
            if post_symptom =="on":

                post_symptoms.append(key.name)
                print(post_symptom)
        disease = []
        
        for sympt in post_symptoms:
            symp = Symptoms.objects.all().filter(name=sympt)
            for sym in symp:
                diseases = Disease.objects.get(name=sym.disease.name)
                disease.append(diseases.name)
        

        disease = list(dict.fromkeys(disease))

        
        context = {'keywords': keywords, 'result': disease}
        return render(request, 'Medilab/logs/diseases_predict.html', context)
    else:

        symptoms = Symptoms.objects.all()
        
        keywords = symptoms
        context = {'keywords': keywords}
        return render(request, 'Medilab/logs/diseases_predict.html', context)
        """

        workpath = os.path.dirname(os.path.abspath(__file__))
        disease_train = pd.read_csv(os.path.join(workpath, "disease.csv"))
        trcols = disease_train.columns
        cols = trcols[:-2]
        train_features = disease_train[cols]
        #train_labels = disease_train['prognosis']
        keywords = list(train_features.keys())
        context = {'keywords': keywords}
        return render(request, 'Medilab/logs/diseases_predict.html', context)
        """




class HelloView(APIView):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        print(incoming_message)


        sms(request)



        return HttpResponse()


@csrf_exempt
def sms(request):
    if request.method == 'POST':

        incoming_message = json.loads(request.body.decode('utf-8'))

        profile = ""
        print(incoming_message)
        print("the_incoming_message")
        income = incoming_message['entry']
        entry = income[-1]
        for message in entry['changes']:
            valu = message['value']

            if 'messages' in valu:

                for contactlist in valu['contacts']:

                    number = contactlist['wa_id']

                    profile = contactlist['profile']['name']

                for messag in valu['messages']:

                    if messag['type'] == 'text':

                        msg = messag['text']['body']





                        msgid = messag['id']

                        datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                        respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

                        print(respo.text)



                        tabol(number, msg, profile)

                    if messag['type'] == 'image':

                        msg = messag['image']['caption']

                        msgid = messag['id']

                        media_id = messag['image']['id']

                        datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                        respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

                        print(respo.text)

                        r = requests.get(f"https://graph.facebook.com/v14.0/{media_id}", headers=head)

                        print(r.json()["url"])


                        media_url = r.json()["url"]

                        r = requests.get(media_url, headers=head)

                        print(r)

                        img = r.content

                        #tabol(number, msg, profile, media_url)

                    if messag['type'] == 'interactive':

                        msgid = messag['id']

                        if messag['interactive']['type'] == 'list_reply':

                            msg = messag['interactive']['list_reply']['id']



                            datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                            respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

                            print(respo.text)

                            tabol(number, msg, profile)
                        if messag['interactive']['type'] == 'button_reply':

                            msg = messag['interactive']['button_reply']['id']



                            datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                            respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

                            print(respo.text)

                            tabol(number, msg, profile)


def tabol(number, mesg, profile, media=None):

    print("now here now")



    main = ("HI *"+ str(profile)+"* \n\nWelcome to Smart Lives Services CHATBOT \n\n"
        "Below is our main menu NB: Click the links below each category or section to get access to that section's menu \n\n ")

    watnum = number[3:]
    print(watnum)
    msg = mesg



    member = homeling.Client.objects.filter(phone=watnum).first()

    print(member.phone)

    careerg = "careerguide"

    print(msg)

    if str(msg) == "hi":

        if member is not None :


            print("Check Now")

            #respons = messenger.send_image(image="https://i.imgur.com/Fh7XVYY.jpeg", recipient_id=number,)





            #print(respons)

            datobj = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                    "text": main
                    },
                    "footer": {
                    "text": "Visit wenextafrica.org"
                    },
                    "action": {
                    "button": "Responces",
                    "sections": [
                        {
                        "title": "Menu",
                        "rows": [
                            {
                            "id": "animalis",
                            "title": "Animals",
                            "description": "Get access to your animal listings" 
                            },
                            {
                            "id": "appointair",
                            "title": "Appointments",
                            "description": "View or Book appointments with the veterinary"
                            },
                            {
                            "id": "reciptair",
                            "title": "Receipts",
                            "description": "View all the receipts"
                            },
                            {
                            "id": "subscriptsair",
                            "title": "Subscriptions",
                            "description": "View all the subscriptions you have made"
                            }
                        ]
                        },

                    ]
                    }
                }
                }




            respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

            print(respo.text)

        else:

            #Change to default

            datobj = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                    "text": main
                    },
                    "footer": {
                    "text": "Visit wenextafrica.org"
                    },
                    "action": {
                    "button": "Responces",
                    "sections": [
                        {
                        "title": "Menu",
                        "rows": [
                            {
                            "id": "animalis",
                            "title": "Animals",
                            "description": "Get access to your animal listings" 
                            },
                            {
                            "id": "appointair",
                            "title": "Appointments",
                            "description": "View or Book appointments with the veterinary"
                            },
                            {
                            "id": "reciptair",
                            "title": "Receipts",
                            "description": "View all the receipts"
                            },
                            {
                            "id": "subscriptsair",
                            "title": "Subscriptions",
                            "description": "View all the subscriptions you have made"
                            }
                        ]
                        },

                    ]
                    }
                }
                }



            respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAANvXaI9edsBAOfN0KKiZC03CHV6t3JpafoAn2aL8wBQIgaaaHEmZBnCK1T2MQvrkShGbQ9T0GiPdQHN1lcxBvq5TQmYc7ZAtHT1SIVDOANYPfsK3Sw9OXohSZBBZAQvt9mS3KRd0w1a1dMB6dIlvsUhj0W1hIwOtt6FC78I4tyhZCZAiYWSGCXQeVzL07f44sZB1n6ZC6j5moQZDZD'} )

            print(respo.text)

    if str(msg) == "animalis":

        animals = Animal.objects.all().filter(user=member.user)

        firstinfo = "View the listing of all the cattle you have registered \n\n "

        print(meetings)


        for animaly in animals:

            animalsingle= "Book: " + animaly.book + ", Tag: "+ animaly.tag + "," + "\n BREED: "+ animaly.breed   + "\n Sex: "+ animaly.sex  + "\n Weight: "+ animaly.weight  + "\n Years: "+ animaly.years  + " \n\n"

            firstinfo = firstinfo + animalsingle



        datobj = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": number,
              "type": "text",
              "text": {
                  "body": firstinfo
              }
              }

        respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

        print(respo.text)

    if str(msg) == "appointair":

        appointments = Appointment.objects.all().filter(user=member.user)
        
        firstinfo = "View the listing of all the appointments you have booked with veterinary \n\n "

        for appointee in appointments:

            appoinmentsingle= "Date: " + appointee.date + "\n Message: "+ appointee.message + "," + "\n Status: "+ appointee.status   + " \n\n"

            firstinfo = firstinfo + appoinmentsingle



        datobj = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": number,
              "type": "text",
              "text": {
                  "body": firstinfo
              }
              }

        respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

        print(respo.text)


    if str(msg) == "reciptair":
        receipts = Sales.objects.all().filter(user=member.user, paid=True)
        
        firstinfo = "View the listing of all the receipts \n\n "

        for receiptee in receipts:

            receiptsingle= "Animal Tag: " + receiptee.animal.tag + "\n Date: "+ receiptee.date + "," + "\n Description: "+ receiptee.description   + "\n Treatment Name: " + receiptee.treatment.name   + "\n Cost: "+ receiptee.treatment.cost  + " \n\n"

            firstinfo = firstinfo + receiptsingle



        datobj = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": firstinfo
            }
            }

        respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

        print(respo.text)


    if str(msg) == "subscriptsair":

        subscriptsees = Subscriptions.objects.all().filter(user=member.user)

        firstinfo = "View the listing of all the subscriptions you have made with veterinary \n\n "

        for subs in subscriptsees:

            receiptsingle= "Payment Date: " + subs.payment_date + "\n Expiry Date: "+ subs.expiry_date + "\n Amount: "+ subs.amount + " \n\n"

            firstinfo = firstinfo + subs



        datobj = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": firstinfo
            }
            }

        respo = requests.post('https://graph.facebook.com/v13.0/109461665230077/messages', json = datobj, headers = {'Authorization' : 'Bearer EAAW9q4zCEWMBAFSuq3ce5pEq0KDoKnn0oWqSDUExH6oJIcoPISEZCD1QakT87RljU1BZASMhggXXOkTigdaAuS5NcvOzJmSyrZAZBqd4p862O2BL6puMWuxoHZCFvv8AzmzXfqyZClzNw1PotbX0NyZAnZAHCMXyljMRrjZABggwFv8XZACQOErZB6VJo0nfThgZAvIDWFqx1qztRNsxjFSWeU3Ko5YAY03hwC8ZD'} )

        print(respo.text)





    
