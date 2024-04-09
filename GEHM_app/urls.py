from django.urls import path

from GEHM_app import views, admin_view, contractor_view, guest

urlpatterns=[
    path('',views.home,name='home'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('registerpage',views.registerpage,name='registerpage'),
    path('guestreg',views.guestreg,name='guestreg'),
    path('adminindex',views.adminindex,name='adminindex'),
    path('conctracor_index',views.conctracor_index,name='conctracor_index'),
    path('guest_emp_index',views.guest_emp_index,name='guest_emp_index'),
    path('logout_view',views.logout_view,name='logout_view'),


    path('contractor_view',admin_view.contractor_view,name='contractor_view'),
    path('guestview',admin_view.guestview,name='guestview'),
    path('job_openinigs',admin_view.job_openinigs,name='job_openinigs'),
    path('del_jobopen/<int:id>/',admin_view.del_jobopen,name='del_jobopen'),
    path('chatpage',admin_view.chatpage,name='chatpage'),
    path('send_message', admin_view.send_message, name='send_message'),
    path('chat_view',admin_view.chat_view,name='chat_view'),
    path('view_contr',admin_view.view_contr,name='view_contr'),
    path('chat_view_gue_admin',admin_view.chat_view_gue_admin,name='chat_view_gue_admin'),
    path('chat_add_ad',admin_view.chat_add_ad,name='chat_add_ad'),
    path('chat_add_ad_gu',admin_view.chat_add_ad_gu,name='chat_add_ad_gu'),
    path('view_sorted',admin_view.view_sorted,name='view_sorted'),
    path('view_all_job_applications', admin_view.view_all_job_applications, name='view_all_job_applications'),
    path('sent_job/<int:id>/', admin_view.sent_job, name='sent_job'),



    path('pay_reg_fee',contractor_view.pay_reg_fee,name='pay_reg_fee'),
    path('con_base',contractor_view.con_base,name='con_base'),
    path('stripe_config',contractor_view.stripe_config,name='stripe_config'),
    path('create_checkout_session',contractor_view.create_checkout_session,name='create_checkout_session'),
    path('payment_view',contractor_view.payment_view,name='payment_view'),
    path('job_view',contractor_view.job_view,name='job_view'),
    path('add_jobpref',contractor_view.add_jobpref,name='add_jobpref'),
    path('view_job',contractor_view.view_job,name='view_job'),
    path('view_profile',contractor_view.view_profile,name='view_profile'),
    path('edit_profile',contractor_view.edit_profile,name='edit_profile'),
    path('search_emp',contractor_view.search_emp,name='search_emp'),
    path('chat_add_con',contractor_view.chat_add_con,name='chat_add_con'),
    path('chat_view_con',contractor_view.chat_view_con,name='chat_view_con'),
    path('chat_base',contractor_view.chat_base,name='chat_base'),
    path('Enquiry_contractor',contractor_view.Enquiry_contractor,name='Enquiry_contractor'),
    path('reply_enquiry/<int:id>/',contractor_view.reply_enquiry,name='reply_enquiry'),
    path('Sort_Employee/<int:id>/',contractor_view.Sort_Employee,name='Sort_Employee'),
    path('add_job_con',contractor_view.add_job_con,name='add_job_con'),
    path('sented_job',contractor_view.sented_job,name='sented_job'),
    path('pay_emp_fee',contractor_view.pay_emp_fee,name='pay_emp_fee'),
    path('payment_viewemp',contractor_view.payment_viewemp,name='payment_viewemp'),



    path('view_contra',guest.view_contra,name='view_contra'),
    path('view_job_guest',guest.view_job_guest,name='view_job_guest'),
    path('Enquiry_add',guest.Enquiry_add,name='Enquiry_add'),
    path('Enquiry_view',guest.Enquiry_view,name='Enquiry_view'),
    path('chat_add_gue',guest.chat_add_gue,name='chat_add_gue'),
    path('chat_view_gue',guest.chat_view_gue,name='chat_view_gue'),
    path('job_list',guest.job_list,name='job_list'),
    path('job_detail/<int:job_id>/',guest.job_detail,name='job_detail'),
    path('apply_job/<int:job_id>/',guest.apply_job,name='apply_job'),
    path('view_payment_gue',guest.view_payment_gue,name='view_payment_gue'),


]