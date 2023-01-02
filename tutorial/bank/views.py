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
class UserFormViewSignUp(View):
    form_class=UserFormUp
    template_name='bank/registration_form_signup.html'
    
    #display blank form
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})
        

    def post(self,request):
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

                
class UserFormViewSignIn(View):
    form_class=UserFormIn
    template_name='bank/registration_form_signin.html'
    
    #display blank form
    def get(self,request):
        form=self.form_class(None)
        print(form)
        return render(request,self.template_name,{'form':form})
        

    def post(self,request):
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




def index(request):
    useraccount=bankdetails.objects.get(username=request.user)
    try:
        creditaccount=creditcarddetails.objects.get(username=request.user)
        creditcard=creditaccount.creditcardnumber
    except:
        creditcard=False

    context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"],"creditcard":creditcard}
    #context={}
    return render(request,'bank/index.html',context)



def logoutButton(request):
   
    logout(request)
    return redirect('bank:signin')


# def MakeTransaction(request):
    
#     return render(request,'bank/transaction_.html',{})

def transactionwithdraw(request):
    useraccount=bankdetails.objects.get(username=request.user)
    context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
    return render(request,'bank/transaction_withdraw.html',context)



def transactionadd(request):
    useraccount=bankdetails.objects.get(username=request.user)
    context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
    return render(request,'bank/transaction_add.html',context)

def Add(request):
    new_transation=transaction()
    new_transation.username=request.user
    useraccount=bankdetails.objects.get(username=request.user)


    new_transation.sender_account_number=useraccount.account_number
    if request.POST['transfer_type']=='self':
        new_transation.reciever_account_number=useraccount.account_number
        new_transation.amount=int(request.POST['amount'])

        new_transation.save()
        useraccount.balance=useraccount.balance+int(request.POST['amount'])
        useraccount.save()
    elif request.POST['transfer_type']=='other':
        new_transation.reciever_account_number=request.POST['otheraccount']
        if useraccount.balance>=int(request.POST['amount']):
            recieveraccount=bankdetails.objects.get(account_number=request.POST['otheraccount'])

            
            new_transation.amount=int(request.POST['amount'])

            new_transation.save()
            useraccount.balance=useraccount.balance-int(request.POST['amount'])
            useraccount.save()
            recieveraccount.balance=recieveraccount.balance+int(request.POST['amount'])
            recieveraccount.save()
    


    

    
    context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
    #context={}
    #return render(request,'bank/index.html',context)
    return redirect('bank:index')

    # new_transation.reciever_account_number
    # new_transation.amount
    # new_transation.transaction_id

   


def withdraw(request):

    useraccount=bankdetails.objects.get(username=request.user)

    if useraccount.balance>=int(request.POST['amount']):
        new_transation=transaction()
        new_transation.username=request.user
        


        new_transation.sender_account_number=useraccount.account_number
        
        new_transation.reciever_account_number=useraccount.account_number

       

        new_transation.amount=int(request.POST['amount'])

        new_transation.save()
        useraccount.balance=useraccount.balance-int(request.POST['amount'])

        useraccount.save()
    
    context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
    #context={}
    # return render(request,'bank/index.html',context)
    return redirect('bank:index')


def statement_download(request):
        transactiondetail=transaction.objects.all()
        df=pd.DataFrame({})
        username=[]
        sender_account_number=[]
        reciever_account_number=[]
        amount=[]
        transaction_id=[]
        useraccount=bankdetails.objects.get(username=request.user)
        for i in transactiondetail:
            # if int(i.transaction_id)==45:
            #     import pdb; pdb.set_trace()
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


        

       
        # df["A"]=[1,2,3,4]
        # df["B"]=[3,4,5,6]
       
        # l=str({"A":1})
        # return HttpResponse([["a","b","c"],["x","y","z"]], status='200',
        #                         content_type='text/csv')

        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="BankStatement.csv"'
        df.to_csv(response, index=False)
        return response
        

def buycreditcard(request):
    creditcard=creditcarddetails()
    creditcard.username=str(request.user)
    useraccount=bankdetails.objects.get(username=request.user)
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

    context={"obj":useraccount,"transaction_field":["reciever_account_number","amount"]}
    #context={}
    #return render(request,'bank/index.html',context)
    return redirect('bank:index')
    

    
    

    



       