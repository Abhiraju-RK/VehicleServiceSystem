from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('garage_home',views.garage_home,name='garage_home'),
    path('user_home',views.user_home,name='user_home'),
    path('user_register',views.user_register,name='user_register'),
    path('garage_register',views.garage_register,name='garage_register'),
    path('login_page',views.login_page,name='login_page'),
    path('logout_page',views.logout_page,name='logout_page'),

    path('add_vehicle_service', views.add_vehicle_service, name='add_vehicle_service'),
    path('book_sevice', views.book_sevice, name='book_sevice'),
    path('view_service_history', views.view_service_history, name='service_history'),
    path('complaint', views.submit_complaint, name='submit_complaint'),

    path('add_service', views.add_service, name='add_service'),
    path('edit_service/<int:service_id>/',views.edit_service,name='edit_service'),
    path('delete_service/<int:service_id>/',views.delete_service,name='delete_service'),
    path('service_list',views.service_list,name='service_list'),
    path('service_view/<int:service_id>/',views.service_view,name='service_view'),
    path('view_bookings', views.view_bookings, name='view_bookings'),
    path('update_booking_status/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),

    path('view_garage_requests/', views.view_garage_requests, name='view_garage_requests'),
    path('approve_garage_request/<int:garage_id>/', views.approve_garage_request, name='approve_garage'),
    path('reject_garage/<int:garage_id>/', views.reject_garage, name='reject_garage'),
    path('view_complaints/', views.view_complaints, name='view_complaints'),

    path('view_users', views.view_users, name='view_users'),
    path('view_all_garages', views.view_all_garages, name='view_all_garages'),
    path('view_all_services', views.view_all_services, name='view_all_services'),
    path('view_vehicles',views.view_vehicles,name='view_vehicles'),

    path('predict_risk/<int:vehicle_id>/',views.predict_risk,name='predict_risk'),
    
]