from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class bankdetails(models.Model):
    username=models.CharField(max_length=20)
    account_number=models.AutoField(primary_key=True)
    balance=models.IntegerField(default=0)
    account_type=models.CharField(default="DEBIT",max_length=200)


    


    # def __str__(self) -> str:
    #     return str(self.account_number)



class transaction(models.Model):
    username=models.CharField(max_length=20)
    sender_account_number=models.CharField(max_length=1000000)
    reciever_account_number=models.CharField(max_length=1000000)
    amount=models.IntegerField()
    transaction_id=models.AutoField(primary_key=True)

    def __str__(self) -> str:
        return str(self.transaction_id)



class creditcarddetails(models.Model):
    username=models.CharField(max_length=20)
    creditcardnumber=models.AutoField(primary_key=True)
    accountnumber=models.CharField(max_length=1000000)
    creditLimit=models.IntegerField(default=50000)
    


