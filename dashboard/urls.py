from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/add/', views.admin_users_add, name='admin_users_add'),
    path('admin/users/<int:user_id>/edit/', views.admin_users_edit, name='admin_users_edit'),
    path('admin/users/<int:user_id>/delete/', views.admin_users_delete, name='admin_users_delete'),
    
    path('admin/trainers/', views.admin_trainers, name='admin_trainers'),
    path('admin/trainers/add/', views.admin_trainers_add, name='admin_trainers_add'),
    path('admin/trainers/<int:user_id>/edit/', views.admin_trainers_edit, name='admin_trainers_edit'),
    path('admin/trainers/<int:user_id>/delete/', views.admin_trainers_delete, name='admin_trainers_delete'),
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/products/add/', views.admin_products_add, name='admin_products_add'),
    path('admin/products/category/add/', views.admin_category_add, name='admin_category_add'),
    path('admin/products/<int:product_id>/edit/', views.admin_products_edit, name='admin_products_edit'),
    path('admin/products/<int:product_id>/delete/', views.admin_products_delete, name='admin_products_delete'),
    
    path('admin/plans/', views.admin_plans, name='admin_plans'),
    path('admin/plans/membership/add/', views.admin_membership_add, name='admin_membership_add'),
    path('admin/plans/membership/<int:plan_id>/edit/', views.admin_membership_edit, name='admin_membership_edit'),
    path('admin/plans/membership/<int:plan_id>/delete/', views.admin_membership_delete, name='admin_membership_delete'),
    
    path('admin/plans/nutrition/add/', views.admin_nutrition_add, name='admin_nutrition_add'),
    path('admin/plans/nutrition/<int:plan_id>/edit/', views.admin_nutrition_edit, name='admin_nutrition_edit'),
    path('admin/plans/nutrition/<int:plan_id>/delete/', views.admin_nutrition_delete, name='admin_nutrition_delete'),
    
    path('admin/plans/goal/add/', views.admin_goal_add, name='admin_goal_add'),
    path('admin/plans/goal/<int:goal_id>/edit/', views.admin_goal_edit, name='admin_goal_edit'),
    path('admin/plans/goal/<int:goal_id>/delete/', views.admin_goal_delete, name='admin_goal_delete'),
    path('admin/payments/', views.admin_payments, name='admin_payments'),
    path('admin/payments/<int:order_id>/', views.admin_payment_detail, name='admin_payment_detail'),
    path('admin/fees/add/', views.admin_fee_add, name='admin_fee_add'),
    path('admin/fees/<int:fee_id>/edit/', views.admin_fee_edit, name='admin_fee_edit'),
    path('admin/messages/', views.admin_messages, name='admin_messages'),
    path('admin/messages/<int:msg_id>/', views.admin_message_detail, name='admin_message_detail'),
    path('admin/messages/<int:msg_id>/resolve/', views.admin_resolve_message, name='admin_resolve_message'),
    path('admin/messages/<int:msg_id>/delete/', views.admin_message_delete, name='admin_message_delete'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),
    
    path('trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/users/', views.trainer_view_users, name='trainer_view_users'),
    path('trainer/assign-workout/', views.trainer_assign_workout, name='trainer_assign_workout'),
    path('trainer/assign-online-workout/', views.trainer_assign_online_workout, name='trainer_assign_online_workout'),
    path('trainer/assign-diet/', views.trainer_assign_diet, name='trainer_assign_diet'),
    path('trainer/assign-online-diet/', views.trainer_assign_online_diet, name='trainer_assign_online_diet'),
    path('trainer/profile/', views.trainer_profile, name='trainer_profile'),
    path('trainer/member/<int:member_id>/progress/', views.view_member_progress, name='view_member_progress'),
    
    path('member/', views.member_dashboard, name='member_dashboard'),
    path('member/profile/', views.member_profile, name='member_profile'),
    path('member/products/', views.member_products, name='member_products'),
    path('member/nutrition/', views.member_nutrition, name='member_nutrition'),
    path('member/goals/', views.member_goals, name='member_goals'),
    path('member/fees/<int:fee_id>/pay/', views.member_pay_fee, name='member_pay_fee'),
    path('member/fees/<int:fee_id>/checkout/', views.member_fee_checkout, name='member_fee_checkout'),
]
