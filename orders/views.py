from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from store.models import Product
from .models import Cart, CartItem, Order
from users.models import Notification


# =========================
# FARMER – VIEW ORDERS
# =========================
@login_required
def farmer_orders(request):
    if request.user.profile.role != 'farmer':
        return redirect('home')

    orders = Order.objects.filter(
        product__farmer=request.user
    ).select_related('product', 'customer')

    return render(request, 'orders/farmer_orders.html', {'orders': orders})


# =========================
# ADD TO CART
# =========================
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart')


# =========================
# VIEW CART
# =========================
@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = []
    total = 0

    if cart:
        items = cart.items.select_related('product')
        total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'orders/cart.html', {'items': items, 'total': total})


# =========================
# UPDATE CART QUANTITY
# =========================
@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            item.quantity = qty
            item.save()

    return redirect('cart')


# =========================
# CHECKOUT
# =========================
@login_required
@transaction.atomic
def checkout(request):
    if request.user.profile.role != 'customer':
        return redirect('home')

    cart = get_object_or_404(Cart, user=request.user)

    for item in cart.items.select_for_update():
        if item.product.stock < item.quantity:
            messages.error(request, "Stock insufficient")
            return redirect('cart')

        Order.objects.create(
            customer=request.user,
            product=item.product,
            quantity=item.quantity
        )

        item.product.stock -= item.quantity
        item.product.save()

    cart.items.all().delete()
    messages.success(request, "Order placed successfully")
    return redirect('home')


# =========================
# CUSTOMER – MY ORDERS
# =========================
@login_required
def my_orders(request):
    if request.user.profile.role != 'customer':
        return redirect('home')

    orders = Order.objects.filter(customer=request.user).select_related('product')
    return render(request, 'orders/my_orders.html', {'orders': orders})


# =========================
# ORDER STATUS MANAGEMENT
# =========================
@login_required
def deliver_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status in ['pending', 'confirmed']:
        order.status = 'delivered'
        order.save()

        send_mail(
            subject='Your order has been delivered 🎉',
            message=f"Hello {order.customer.username},\n\n"
                    f"Your order for {order.product.name} has been delivered successfully.\n"
                    f"Quantity: {order.quantity}\n\n"
                    "Thank you for shopping with FarmFresh 🌱",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.customer.email],
            fail_silently=True
        )

    return redirect('farmer_orders')


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()

        send_mail(
            subject='Your order has been cancelled ❌',
            message=f"Hello {order.customer.username},\n\n"
                    f"Your order for {order.product.name} has been cancelled by the farmer.\n\n"
                    "If you have questions, please contact support.\n"
                    "FarmFresh 🌱",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.customer.email],
            fail_silently=True
        )

    return redirect('farmer_orders')


# =========================
# GENERATE PDF INVOICE
# =========================
@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    p.drawString(50, 800, "FarmFresh Invoice")
    p.drawString(50, 770, f"Order ID: {order.id}")
    p.drawString(50, 750, f"Customer: {order.customer.username}")
    p.drawString(50, 730, f"Product: {order.product.name}")
    p.drawString(50, 710, f"Quantity: {order.quantity}")
    p.drawString(50, 690, f"Status: {order.status}")
    p.drawString(50, 670, f"Date: {order.ordered_at.strftime('%d-%m-%Y')}")
    p.drawString(50, 620, "Thank you for shopping with FarmFresh 🌱")

    p.showPage()
    p.save()

    return response


# =========================
# PLACE ORDER WITH NOTIFICATION
# =========================
@login_required
def place_order(request):
    if request.method == 'POST':
        # Set your logic for selected_product, selected_farmer, and calculated_total
        order = Order.objects.create(
            customer=request.user,
            farmer=selected_farmer,
            product=selected_product,
            quantity=request.POST['quantity'],
            total_amount=calculated_total,
            status='Pending'
        )

        # Notify the farmer
        Notification.objects.create(
            user=order.farmer,
            message=f"New order #{order.id} placed by {request.user.username}."
        )

        return redirect('customer_home')

    return render(request, 'orders/place_order.html')


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, farmer=request.user)
    new_status = request.POST.get('status')  # e.g., 'delivered'
    order.status = new_status
    order.save()

    if new_status.lower() == 'delivered':
        # ✅ Notify customer
        Notification.objects.create(
            user=order.customer,
            message=f"Your order #{order.id} has been delivered. Invoice is ready for download."
        )

    return redirect('farmer_orders')
