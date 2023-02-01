from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("admin", views.admin, name="admin"),
    path("register", views.register, name="register"),
    path("animal_reg", views.animal_reg, name="animal_reg"),
    path("receipt", views.receipt, name="receipt"),
    path("appointment_reg", views.appointment_reg, name="appointment_reg"),
    path("treatment", views.treatment, name="treatment"),
    path("animalReg", views.animalReg, name="animalReg"),
    path("animalRegAdmin", views.animalRegAdmin, name="animalRegAdmin"),
    path("appointment", views.appointment, name="appointment"),
    path("appointmentAdmin", views.appointmentAdmin, name="appointmentAdmin"),
    path("sales", views.sales, name="sales"),
    path("sms", views.sms, name="sms"),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path("logout", views.logout, name="logout"),
    path("prediction", views.prediction, name="prediction"),
    path("invoice", views.invoice, name="invoice"),
    path("subscriptions", views.subscriptions, name="subscriptions"),
    path("subscriptionsPay", views.subscriptionsPay, name="subscriptionsPay"),
    path("animalReport", views.animalReport, name="animalReport"),
    path("salesAdmin", views.salesAdmin, name="salesAdmin"),
]