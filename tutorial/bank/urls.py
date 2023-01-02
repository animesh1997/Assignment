from django.urls import path,include,re_path
from . import views
app_name="bank"



# user_list = views.usersignup_rest.as_view({
#     'get': 'list',
#     'post': 'create'
# })
urlpatterns = [
    path('signin/',views.UserFormViewSignIn.as_view(),name="signin"),
    path('signup/',views.UserFormViewSignUp.as_view(),name="signup"),
    #path('signup_rest/',views.usersignup_rest.as_view({'post': 'create'}),name="signup_rest"),
    path('logout/',views.logoutButton,name="logout"),
    path('index/',views.index,name="index"),
    path('add/',views.Add,name="add"),
    path('withdraw/',views.withdraw,name="withdraw"),   
    path('transactionadd/',views.transactionadd,name="transactionadd"),
    path('transactionwithdraw/',views.transactionwithdraw,name="transactionwithdraw"),
    path('download/',views.statement_download,name="download"),
    path('buycredit/',views.buycreditcard,name="buycredit"),
]
