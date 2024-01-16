import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import orders
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.

def invoice(request,order_id):
    order=orders.objects.get(id=order_id)
    print(order.order_date)
    if order.address:
        address_detail=json.loads(order.address)
    else:
        address_detail={}
    order_products=order.order_itemss.all()
    
    context={
        'order':order,
        'products':order_products,
        'address':address_detail
    }
    if order.offer_applied:
        discount_amount=order.sub_total - order.offer_price
        context['dicount']=discount_amount
    return render(request,'invoice.html',context)


def pdf_creat(request,order_id):
    order=orders.objects.get(id=order_id)
    if order.address:
        address_detail=json.loads(order.address)
    else:
        address_detail={}
    order_products=order.order_itemss.all()
    
    context={
        'order':order,
        'products':order_products,
        'address':address_detail
    }
    if order.offer_applied:
        discount_amount=order.sub_total - order.offer_price
        context['dicount']=discount_amount
    template_path='invoice.html'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

