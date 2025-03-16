from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer,Supplier,Invoice
from django.core.paginator import Paginator

#supplier= provedores
def index(request):
    
    
    return render(request, 'inicio.html')


def supplier_list(request):
    
    suppliers = Supplier.objects.all()
    context = {
        'suppliers': suppliers,
    }
    return render(request, 'proveedores.html', context)


def supplier_info(request, supplier_id):
    # Intentar obtener el proveedor
    supplier = Supplier.objects.get(id=supplier_id)
    

    if not supplier:
        # Si el proveedor no existe, renderizar una página de error personalizada
        return render(request, 'error.html', {'message': 'El proveedor no existe.'}, status=404)

    # Obtener todas las facturas asociadas a ese proveedor
    invoices = Invoice.objects.filter(supplier=supplier).order_by('id')  # Orden ascendente por ID
    paginated = Paginator(invoices, 2)
    page_number = request.GET.get('page') #Get the requested page number from the URL
    
    page_invoices = paginated.get_page(page_number)



    customer=Customer.objects.all()
    

    # Pasar los datos al template
    context = {
        'supplier':supplier,
        'page':page_invoices,
        'customers': customer,
    }

    return render(request, 'Invoice.html', context)





def invoice_detail(request, invoice_id):
    # Obtener la factura con el ID proporcionado o mostrar error 404 si no existe
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # Obtener el proveedor (vendedor) de la factura
    supplier = invoice.supplier

    # Obtener el cliente de la factura (asumiendo que hay un campo 'client' en Invoice)
    client = invoice.customer
    customers=Customer.objects.all()

    # Pasar los datos al template
    context = {
        'invoice': invoice,
        'supplier': supplier,
        'client': client,
        'customers':customers
    }

    return render(request, 'invoiceDetail.html', context)






from django.http import HttpResponse
from reportlab.pdfgen import canvas
   
def download_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{invoice.invoice_number}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Factura #{invoice.invoice_number}")
    p.drawString(100, 780, f"Fecha: {invoice.invoice_date}")
    p.drawString(100, 760, f"Monto: ${invoice.amount}")
    p.drawString(100, 740, f"Estado: {'Electrónica' if invoice.status_electronics else 'No electrónica'}")
    p.showPage()
    p.save()

    return response


def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        invoice_number = request.POST.get('invoice_number')
        customer_id = request.POST.get('customer')
        invoice_date = request.POST.get('invoice_date')
        amount = request.POST.get('amount')  # Añadido campo de monto
        status_electronics = request.POST.get('status_electronics') == 'True'
        
        # Actualizar la factura
        invoice.invoice_number = invoice_number
        invoice.customer = get_object_or_404(Customer, id=customer_id)
        invoice.invoice_date = invoice_date
        invoice.amount = amount 
        invoice.status_electronics = status_electronics
        # Manejar la carga de la nueva imagen
        if 'image' in request.FILES:
            # Asignar la nueva imagen
            invoice.image = request.FILES['image']
            
        
        
        invoice.save()
        
        
        return redirect('proveedores:invoice', invoice_id=invoice.id)
    
    # Si es GET, redirigir a la página de detalle
    return redirect('proveedores:invoice', invoice_id=invoice.id)


def delete_invoice(request,invoice_id):

    invoice = get_object_or_404(Invoice, id=invoice_id)
    supplier=invoice.supplier
    supplier_id=supplier.id
    print( supplier_id)

    if request.method == 'POST':
        invoice.delete()
        
        return redirect('proveedores:proveedor',supplier_id) 
    
    supplier=Invoice.supplier
    return redirect('proveedores:invoice', invoice_id) 


def SaveInvoice(request,supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        invoice_number = request.POST.get('invoice_number')
        customer_id = request.POST.get('customer')
        invoice_date = request.POST.get('invoice_date')
        amount = request.POST.get('amount')  # Añadido campo de monto
        status_electronics = request.POST.get('status_electronics') 
        image=request.FILES['image']
        # Actualizar la factura
        
        invoice=Invoice()
        invoice.supplier=supplier
        invoice.invoice_number = invoice_number
        invoice.customer = get_object_or_404(Customer, id=customer_id)
        invoice.invoice_date = invoice_date
        invoice.amount = amount 
        invoice.status_electronics = status_electronics
        invoice.image = image
        # Manejar la carga de la nueva imagen
        
            
        
        
        invoice.save()
        
        
        
    # Si es GET, redirigir a la página de detalle
    return redirect('proveedores:proveedor', supplier_id=supplier.id)


def SaveSupplier(request):
    
    if request.method == 'POST':
        # Obtener datos del formulario
        company=request.POST['company']
        first_name = request.POST['first_name']
        description = request.POST['description']
        address=request.POST['address']
        phone=request.POST['phone']
        email=request.POST['email']

        logo=request.FILES['image']
        # Actualizar la factura
        
        supplier=Supplier()
        supplier.company=company
        supplier.first_name = first_name
        supplier.description = description
        supplier.address=address
        supplier.phone=phone
        supplier.email=email
        supplier.logo=logo

        # Manejar la carga de la nueva imagen
        
            
        
        
        supplier.save()
        
        
        
    
    return redirect('proveedores:proveedores')
 