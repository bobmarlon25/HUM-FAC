from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer,Supplier,Invoice
from django.core.paginator import Paginator

from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.utils import timezone

import json
from django.core.serializers.json import DjangoJSONEncoder

#supplier= provedores
def index(request):
    # Obtener parámetros de filtro
    year = request.GET.get('year')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Construir filtros dinámicos
    filters = {}

    if year:
        filters['invoice_date__year'] = year
    if fecha_inicio:
        filters['invoice_date__gte'] = fecha_inicio
    if fecha_fin:
        filters['invoice_date__lte'] = fecha_fin

    # Aplicar filtros directamente en la query
    facturas_query = Invoice.objects.filter(**filters)
    
    # Conteos básicos
    total_proveedores = Supplier.objects.count()
    total_facturas = facturas_query.count()
    total_compradores = Customer.objects.count()

    # Calcular valor total de facturas
    valor_total = facturas_query.aggregate(total=Sum('amount'))['total'] or 0
    
    # Obtener años disponibles para el filtro
    years = Invoice.objects.dates('invoice_date', 'year').values_list('invoice_date__year', flat=True).distinct()

     # Datos para gráfico de facturas por mes (del año actual o filtrado)
    if year:
        year_filter = int(year)
    else:
        year_filter = timezone.now().year
    
    facturas_por_mes = (
        facturas_query.filter(invoice_date__year=year_filter)
        .annotate(mes=TruncMonth('invoice_date'))
        .values('mes')
        .annotate(
            cantidad=Count('id'),
            valor_total=Sum('amount')
        )
        .order_by('mes')
    )
    
    # Preparar datos para el gráfico
    meses = []
    cantidades = []
    valores = []
    
    # Inicializar con ceros para todos los meses
    for i in range(1, 13):
        meses.append(datetime(year_filter, i, 1).strftime('%b'))
        cantidades.append(0)
        valores.append(0)
    
    # Llenar con datos reales
    for item in facturas_por_mes:
        mes_index = item['mes'].month - 1  # Ajustar a índice 0-11
        cantidades[mes_index] = item['cantidad']
        valores[mes_index] = float(item['valor_total'])
    
    # Datos para encargados
    encargados_data = (
        facturas_query
        .values('customer')
        .annotate(
            total_facturas=Count('id'),
            valor_total=Sum('amount'),
            promedio=Avg('amount')
        )
        .order_by('-valor_total')
    )
    
    # Calcular porcentajes
    encargados = []
    for encargado in encargados_data:
        porcentaje = (encargado['valor_total'] / valor_total * 100) if valor_total > 0 else 0
        encargados.append({
            'nombre': str(encargado['customer']),
            'total_facturas': encargado['total_facturas'],
            'valor_total': encargado['valor_total'],
            'promedio': encargado['promedio'],
            'porcentaje': round(porcentaje, 1)
        })


   # Preparar datos para el gráfico de distribución por encargado
    nombres_encargados = [e['nombre'] for e in encargados]
    valores_encargados = [float(e['valor_total']) for e in encargados]

    

    context = {
        "total_prov": total_proveedores,
        "total_fact": total_facturas,
        "total_comp": total_compradores,
        "valor_total": f"${valor_total:,.2f}",
        "years": years,
        "selected_year": year,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "encargados": encargados,
        
        # Datos para gráficos en formato JSON
        "datos_meses": {
            "labels": meses,
            "cantidades": cantidades,
            "valores": valores
        },
        "datos_encargados": {
            "nombres": nombres_encargados,
            "valores": valores_encargados
        }
    
    }
    return render(request, 'inicio.html',context)




def inde(request):
   # Obtener parámetros de filtro
    year = request.GET.get('year')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Construir filtros dinámicos
    filters = {}

    if year:
        filters['fecha__year'] = year
    if fecha_inicio:
        filters['fecha__gte'] = fecha_inicio
    if fecha_fin:
        filters['fecha__lte'] = fecha_fin

    # Aplicar filtros directamente en la query
    facturas_query = Invoice.objects.filter(**filters)
    
    # Conteos básicos
    total_proveedores = Supplier.objects.count()
    total_facturas = facturas_query.count()
    total_compradores = Customer.objects.count()
    
    # Calcular valor total de facturas
    valor_total = facturas_query.aggregate(total=Sum('amount'))['total'] or 0
    
    # Obtener años disponibles para el filtro
    years = Invoice.objects.dates('fecha', 'year').values_list('fecha__year', flat=True).distinct()
    
    # Datos para gráfico de facturas por mes (del año actual o filtrado)
    if year:
        year_filter = int(year)
    else:
        year_filter = timezone.now().year
    
    facturas_por_mes = (
        facturas_query.filter(fecha__year=year_filter)
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(
            cantidad=Count('id'),
            valor_total=Sum('valor')
        )
        .order_by('mes')
    )
    
    # Preparar datos para el gráfico
    meses = []
    cantidades = []
    valores = []
    
    # Inicializar con ceros para todos los meses
    for i in range(1, 13):
        meses.append(datetime(year_filter, i, 1).strftime('%b'))
        cantidades.append(0)
        valores.append(0)
    
    # Llenar con datos reales
    for item in facturas_por_mes:
        mes_index = item['mes'].month - 1  # Ajustar a índice 0-11
        cantidades[mes_index] = item['cantidad']
        valores[mes_index] = float(item['valor_total'])
    
    # Datos para encargados
    encargados_data = (
        facturas_query
        .values('encargado')
        .annotate(
            total_facturas=Count('id'),
            valor_total=Sum('valor'),
            promedio=Avg('valor')
        )
        .order_by('-valor_total')
    )
    
    # Calcular porcentajes
    encargados = []
    for encargado in encargados_data:
        porcentaje = (encargado['valor_total'] / valor_total * 100) if valor_total > 0 else 0
        encargados.append({
            'nombre': encargado['encargado'],
            'total_facturas': encargado['total_facturas'],
            'valor_total': encargado['valor_total'],
            'promedio': encargado['promedio'],
            'porcentaje': round(porcentaje, 1)
        })
    
    # Últimas facturas
    ultimas_facturas = (
        facturas_query
        .select_related('proveedor')  # Asumiendo que hay una relación con proveedor
        .order_by('-fecha')[:5]
    )
    
    # Preparar datos para las últimas facturas
    facturas_formateadas = []
    for factura in ultimas_facturas:
        facturas_formateadas.append({
            'numero': factura.numero,
            'fecha': factura.fecha,
            'proveedor': factura.proveedor.nombre if hasattr(factura, 'proveedor') else '',
            'encargado': factura.encargado,
            'valor': factura.valor,
            'estado': factura.estado if hasattr(factura, 'estado') else 'Pendiente'
        })
    
    # Preparar datos para el gráfico de distribución por encargado
    nombres_encargados = [e['nombre'] for e in encargados]
    valores_encargados = [float(e['valor_total']) for e in encargados]


    # Después de calcular los encargados
    
    
    # Contexto para la plantilla
    context = {
        "total_prov": total_proveedores,
        "total_fact": total_facturas,
        "total_comp": total_compradores,
        "valor_total": f"${valor_total:,.2f}",
        "years": years,
        "selected_year": year,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "encargados": encargados,
        "ultimas_facturas": facturas_formateadas,
        # Datos para gráficos en formato JSON
        "datos_meses": {
            "labels": meses,
            "cantidades": cantidades,
            "valores": valores
        },
        "datos_encargados": {
            "nombres": nombres_encargados,
            "valores": valores_encargados
        }
    }
    
    return render(request, 'inicio.html', context)

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
 