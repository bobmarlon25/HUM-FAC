
from django.urls import path
from . import views 

app_name='proveedores'



urlpatterns = [
    path('',views.index,name='index'),
    path('proveedores',views.supplier_list,name='proveedores'),
    path('proveedor/<int:supplier_id>',views.supplier_info,name='proveedor'),
    path('invoice/<int:invoice_id>',views.invoice_detail,name='invoice'),
   path('download_invoice_pdf/<int:invoice_id>',views.download_invoice_pdf,name='download_invoice_pdf'),
   path('invoice/<int:invoice_id>/edit/', views.edit_invoice, name='edit_invoice'),
    path('invoice/delete_invoice/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('proceedor/<int:supplier_id>/saveInvoice/', views.SaveInvoice, name='saveInvoice'),
    path('savesupplier', views.SaveSupplier, name='savesupplier')
    
]


