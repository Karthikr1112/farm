from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
import csv
import json
from .models import Inquiry

def landing_page(request):
    return render(request, 'core/landing.html')

@csrf_exempt
def submit_inquiry(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            name = data.get('name')
            phone = data.get('phone')
            category = data.get('category')
            product = data.get('product')
            message = data.get('message', '')

            if not all([name, phone, category, product]):
                return JsonResponse({'status': 'error', 'message': 'All required fields must be filled.'}, status=400)

            inquiry = Inquiry.objects.create(
                name=name,
                phone=phone,
                category=category,
                product=product,
                message=message
            )

            # Generate WhatsApp inquiry link
            whatsapp_msg = f"Hello Uzhavan Valam, I am {name} ({category}). I would like to inquire about {product}."
            whatsapp_url = f"https://wa.me/919944634026?text={whatsapp_msg.replace(' ', '%20')}"

            return JsonResponse({
                'status': 'success',
                'message': 'Inquiry successfully saved!',
                'whatsapp_url': whatsapp_url
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def orders_dashboard(request):
    inquiries = Inquiry.objects.all().order_by('-created_at')
    
    total_leads = inquiries.count()
    completed_leads = inquiries.filter(status='Completed').count()
    active_leads = total_leads - completed_leads
    
    # Calculate statistics for charts
    category_counts = list(Inquiry.objects.values('category').annotate(count=Count('id')))
    product_counts = list(Inquiry.objects.values('product').annotate(count=Count('id')))
    
    categories = [item['category'] for item in category_counts]
    cat_data = [item['count'] for item in category_counts]
    
    products = [item['product'] for item in product_counts]
    prod_data = [item['count'] for item in product_counts]

    context = {
        'inquiries': inquiries,
        'total_leads': total_leads,
        'completed_leads': completed_leads,
        'active_leads': active_leads,
        'categories_js': json.dumps(categories),
        'cat_data_js': json.dumps(cat_data),
        'products_js': json.dumps(products),
        'prod_data_js': json.dumps(prod_data),
    }
    return render(request, 'core/dashboard.html', context)

def complete_order(request, order_id):
    inquiry = get_object_or_404(Inquiry, id=order_id)
    inquiry.status = 'Completed' if inquiry.status == 'Active' else 'Active'
    inquiry.save()
    return redirect('orders_dashboard')

def delete_order(request, order_id):
    inquiry = get_object_or_404(Inquiry, id=order_id)
    inquiry.delete()
    return redirect('orders_dashboard')

def export_orders_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="natural_village_orders.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Phone', 'Category', 'Product', 'Message', 'Status', 'Date Submitted'])
    
    for inquiry in Inquiry.objects.all().order_by('-created_at'):
        writer.writerow([
            inquiry.id,
            inquiry.name,
            inquiry.phone,
            inquiry.category,
            inquiry.product,
            inquiry.message,
            inquiry.status,
            inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
        
    return response

def order_page(request):
    return render(request, 'core/order.html')

