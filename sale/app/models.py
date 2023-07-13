from datetime import datetime
import email
from pyexpat import model
from sqlite3 import Time
from django.utils import timezone
from time import timezone
from django.db import models

# Create your models here.

class User(models.Model):
    userID = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField( max_length=128,blank=True, null=True)
    phoneNumber = models.CharField(max_length=11,unique= True)
    codeMelli = models.CharField(max_length=11, unique= True)
    userName = models.CharField( max_length=15 , unique= True, default= "phoneNumber")
    password = models.CharField( max_length=15 , default= "codeMelli")
    address = models.CharField( max_length=256 ,blank=True, null=True)
    email = models.EmailField( blank=True, null=True)
    telephone_sabet = models.CharField(max_length=11, unique= True, blank=True, null=True)
    Type_CHoice = (
        ("user", "User"), 
        ("admin", "Admin"), 
    )
    Register_Status_CHoice = (
        ("not register yet", "NotRegisterYET"), 
        ("registered", "Registered"), 
        ("non-register", "NonRegister"), 
    )
    U_Type = models.CharField(max_length=16 ,choices=Type_CHoice, default="user")
    Register_Status = models.CharField(max_length=16 ,choices=Register_Status_CHoice, default="not register yet")
    # birthDate = models.DateField(null=True, blank=True)
    # phoneNumber = models.IntegerField(min_length=10,max_length=11)
    def __str__(self) -> str:
        return (self.name + " - type: " + self.U_Type) + "---ID: " + str(self.userID)

class Good(models.Model):
    g_description = models.CharField(max_length=128)
    def __str__(self) -> str:
        return self.g_description

class Design(models.Model):
    d_description = models.CharField(max_length=128)
    def __str__(self) -> str:
        return self.d_description

class Color(models.Model):
    c_description = models.CharField(max_length=128)
    def __str__(self) -> str:
        return self.c_description

class customer_order(models.Model):
    U_userID = models.IntegerField(default=0)
    # U_userID = models.ForeignKey(User, related_name='userID2', on_delete=models.CASCADE)
    good_description = models.CharField(max_length=128 , default= "")
    color_description = models.CharField(max_length=128, default="",null=True, blank=True)
    design_description = models.CharField(max_length=128, default="",null=True, blank=True)
    width = models.FloatField(default=0,null=True, blank=True)
    length = models.FloatField(default=0,null=True, blank=True)
    thickness = models.FloatField(default=0,null=True, blank=True)
    count = models.IntegerField()
    registration_date = models.DateTimeField(default= datetime.now, blank=True)
    orderID = models.AutoField(auto_created=True, primary_key=True)
    orderNumber = models.IntegerField(default=0)
    Order_Status_CHoice = (
        ("sabt shode", "sabt shode"), 
        ("taeed shode", "taeed shode"), 
        ("rad shode", "rad shode"), 
        ("ersal baraye tolid", "ersal baraye tolid"), 
        ("tahvil dade shode", "tahvil dade shode"), 
    )
    Order_Status = models.CharField(max_length=28 ,choices=Order_Status_CHoice, default="sabt shode")
    text_adminToadmin = models.CharField(max_length=256, default="-",null=True, blank=True)
    text_adminTouser = models.CharField(max_length=256, default="-",null=True, blank=True)
    tozihat_1order = models.CharField(max_length=256, default="-",null=True, blank=True)
    tozihat_5orders = models.CharField(max_length=256, default="-",null=True, blank=True)
    def __str__(self) -> str:
        return "orderID: " + str(self.orderID) + " - orderNumber: " + str(self.orderNumber)