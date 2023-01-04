from io import StringIO
from typing import IO
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views import generic

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from .forms import UserFormIn,UserFormUp
from bank.models  import bankdetails,transaction,creditcarddetails
import uuid
import pandas as pd
from django.contrib import messages



#--------------------------------------------------------------------------------------------------------------------
# from rest_framework import viewsets
# from django.contrib.auth.models import User
# from bank.serializers import UserSerializer
# from rest_framework import generics
# from rest_framework import permissions
# #from Bank.permissions  import IsOwnerOrReadOnly
# from rest_framework.renderers import TemplateHTMLRenderer

# class usersignup_rest(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     renderer_classes=[TemplateHTMLRenderer]
#     template_name='bank/registration_form_signup.html'
#     #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#--------------------------------------------------------------------------------------------------------------------

# Create your views here.
def error(request):

    return render(request,'bank/error.html',{})

def home(request):

    return render(request,'bank/home.html',{})


class UserFormViewSignUp(View):
    form_class=UserFormUp
    template_name='bank/registration_form_signup.html'
    
    #display blank form
    def get(self,request):
        try:
            form=self.form_class(None)
            return render(request,self.template_name,{'form':form})
        except Exception as e:
            context={"error":e}
            return render(request,'bank/error.html',context)
        

    def post(self,request):
        try:
            form=self.form_class(request.POST)

            if form.is_valid():
                user=form.save(commit=False)

                ### clean /normalize the data
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                confirmpassword=form.cleaned_data['confirmpassword']
                if password==confirmpassword:
                    user.set_password(password)
                    user.save()

                    createAccount=bankdetails()
                    createAccount.username=username
                    if not bankdetails.objects.first():
                        createAccount.account_number=10000

                    #createAccount.account_number=   uuid.uuid4().int
                    createAccount.save()

                    return redirect('bank:signin')


                else:
                    form=self.form_class(None)
                    
                    return render(request,self.template_name,{'form':form})
            else:

                form=self.form_class(None)
                    
                return render(request,self.template_name,{'form':form})
        except Exception as e:
            context={"error":e}
            return render(request,'bank/error.html',context)

                
class UserFormViewSignIn(View):
    form_class=UserFormIn
    template_name='bank/registration_form_signin.html'
    
    #display blank form
    def get(self,request):
        try:
            form=self.form_class(None)
        
            return render(request,self.template_name,{'form':form})

        except Exception as e:
            context={"error":e}
            return render(request,'bank/error.html',context)
        

    def post(self,request):
        try:
            form=self.form_class(request.POST)

            # if form.is_valid():
            #     user=form.save(commit=False)

            #     ### clean /normalize the data
            #     username=form.cleaned_data['username']
            #     password=form.cleaned_data['password']

                #user.set_password(password)
                #user.save()
                

            user=authenticate(username=request.POST['username'],password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    #logout(request,user)
                    return redirect('bank:index')

            else:
                return redirect('bank:signin')
        except Exception as e:
            context={"error":e}
            return render(request,'bank/error.html',context)




def index(request):
    try:
        useraccount=bankdetails.objects.get(username=request.user)
        try:
            creditaccount=creditcarddetails.objects.get(username=request.user)
            creditcard=creditaccount.creditcardnumber
        except:
            creditcard=False

        context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"],"creditcard":creditcard}
        #context={}
        return render(request,'bank/index.html',context)
    except Exception as e:
        context={"error":"InvalidUser Please login"}
        return render(request,'bank/error.html',context)




def logoutButton(request):
    try:
        logout(request)
        return redirect('bank:home')
    except Exception as e:
        context={"error":e}
        return render(request,'bank/error.html',context)


# def MakeTransaction(request):
    
#     return render(request,'bank/transaction_.html',{})

def transactionwithdraw(request):
    try:
        useraccount=bankdetails.objects.get(username=request.user)
        context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
        return render(request,'bank/transaction_withdraw.html',context)

    except Exception as e:
        context={"error":e}
        return render(request,'bank/error.html',context)



def transactionadd(request):
    try:
        useraccount=bankdetails.objects.get(username=request.user)
        context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
        return render(request,'bank/transaction_add.html',context)
    except Exception as e:
        context={"error":e}
        return render(request,'bank/error.html',context)


def transaction_transfer(request):
    try:
        useraccount=bankdetails.objects.get(username=request.user)
        context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
        return render(request,'bank/transaction_transfer.html',context)
    except Exception as e:
        context={"error":e}
        return render(request,'bank/error.html',context)



def Add(request):
    try:
        new_transation=transaction()
        new_transation.username=request.user
        try:
            useraccount=bankdetails.objects.get(username=request.user)
        except Exception as e:
            context={"error":"InvalidUser Please login"}
            return render(request,'bank/error.html',context)

        new_transation.sender_account_number=useraccount.account_number
    
        new_transation.reciever_account_number=useraccount.account_number
        new_transation.amount=int(request.POST['amount'])

        new_transation.save()
        useraccount.balance=useraccount.balance+int(request.POST['amount'])
        useraccount.save()

        context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
        #context={}
        #return render(request,'bank/index.html',context)
        return redirect('bank:index')

    except Exception as e:
        context={"error":e}
        return render(request,'bank/error.html',context)


def transfer(request):
    try:
        new_transation=transaction()
        new_transation.username=request.user
        try:
            useraccount=bankdetails.objects.get(username=request.user)
        except Exception as e:
            context={"error":"InvalidUser Please login"}
            return render(request,'bank/error.html',context)


        new_transation.sender_account_number=useraccount.account_number
        
        new_transation.reciever_account_number=request.POST['otheraccount']
        try:
            if useraccount.balance>=int(request.POST['amount']):
                recieveraccount=bankdetails.objects.get(account_number=request.POST['otheraccount'])

                
                new_transation.amount=int(request.POST['amount'])

                new_transation.save()
                useraccount.balance=useraccount.balance-int(request.POST['amount'])
                useraccount.save()
                recieveraccount.balance=recieveraccount.balance+int(request.POST['amount'])
                recieveraccount.save()

            else:
                messages.add_message(request, messages.INFO, 'Insufficient Balance')
                try:
                    useraccount=bankdetails.objects.get(username=request.user)
                    context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
                    return render(request,'bank/transaction_transfer.html',context)
                except Exception as e:
                    context={"error":e}
                    return render(request,'bank/error.html',context)

        except Exception as e:
            context={"error":"RecieverAcccount Invalid "}
            return render(request,'bank/error.html',context)

        
        


        

        
        context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
        #context={}
        #return render(request,'bank/index.html',context)
        return redirect('bank:index')
    except Exception as e:
        context={"error":e}
        return render(request,'bank/error.html',context)



def withdraw(request):
    try:
        try:
            useraccount=bankdetails.objects.get(username=request.user)
        except Exception as e:
            context={"error":"Invalid User Please login"}
            return render(request,'bank/error.html',context)

        if useraccount.balance>=int(request.POST['amount']):
            new_transation=transaction()
            new_transation.username=request.user
            


            new_transation.sender_account_number=useraccount.account_number
            
            new_transation.reciever_account_number=useraccount.account_number

        

            new_transation.amount=int(request.POST['amount'])

            new_transation.save()
            useraccount.balance=useraccount.balance-int(request.POST['amount'])

            useraccount.save()

        else:
            #pass
            messages.add_message(request, messages.INFO, 'Insufficient Balance')
            try:
                useraccount=bankdetails.objects.get(username=request.user)
                context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
                return render(request,'bank/transaction_withdraw.html',context)

            except Exception as e:
                context={"error":e}
                return render(request,'bank/error.html',context)
        
        context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
        #context={}
        # return render(request,'bank/index.html',context)
        return redirect('bank:index')
    except Exception as e:
        context={"error":e}
        return render(request,'bank/error.html',context)



def statement_download(request):
        try:
            transactiondetail=transaction.objects.all()
            df=pd.DataFrame({})
            username=[]
            sender_account_number=[]
            reciever_account_number=[]
            amount=[]
            transaction_id=[]
            try:
                useraccount=bankdetails.objects.get(username=request.user)
            except Exception as e:
                context={"error":"InvalidUser Please login"}
                return render(request,'bank/error.html',context)
            for i in transactiondetail:
                if int(i.sender_account_number)==int(useraccount.account_number) or int(i.reciever_account_number)==int(useraccount.account_number):
                
                    username.append(i.username)
                    sender_account_number.append(i.sender_account_number)
                    reciever_account_number.append(i.reciever_account_number)
                    amount.append(i.amount)
                    transaction_id.append(i.transaction_id)


            df['username']=username
            df['sender_account_number']=sender_account_number
            df['reciever_account_number']=reciever_account_number
            df['amount']=amount
            df['transaction_id']=transaction_id

            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="BankStatement.csv"'
            df.to_csv(response, index=False)
            return response
        except Exception as e:
            context={"error":e}
            return render(request,'bank/error.html',context)


def buycreditcard(request):
    try:
        creditcard=creditcarddetails()
        creditcard.username=str(request.user)
        try:
            useraccount=bankdetails.objects.get(username=request.user)
        except Exception as e:
            context={"error":"InvaildUser"}
            return render(request,'bank/error.html',context)
        creditcard.accountnumber=useraccount.account_number
        if not creditcarddetails.objects.first():
            creditcard.creditcardnumber=10000


        ### cost of credit card be 500
        ### taking credit card buy reciever acc number as 100
    
        if useraccount.balance>=500:
            new_transation=transaction()
            new_transation.username=request.user
            


            new_transation.sender_account_number=useraccount.account_number
            
            new_transation.reciever_account_number=100

        

            new_transation.amount=500

            new_transation.save()
            useraccount.balance=useraccount.balance-500

            useraccount.save()
            creditcard.save()
        else:
            pass
            ## add Alert

        context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
        #context={}
        #return render(request,'bank/index.html',context)
        return redirect('bank:index')
    except Exception as e:
            context={"error":e}
            return render(request,'bank/error.html',context)

    
    

    



       