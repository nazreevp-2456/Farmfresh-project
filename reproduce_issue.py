import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\nazre\Desktop\Entry\Django\FarmFresh')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmFresh.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from store.models import Product
from orders.models import Order
from django.core.files.uploadedfile import SimpleUploadedFile

def test_flow():
    print("--- Starting Reproduction Test ---")
    
    # Clean up previous test data
    User.objects.filter(username='farmer_bob').delete()
    User.objects.filter(username='customer_alice').delete()
    print("Cleaned up old users.")

    # 1. Register Farmer
    try:
        farmer_user = User.objects.create_user(username='farmer_bob', email='bob@example.com', password='password123')
        # Simulate form saving which updates profile role
        # Note: Signal should have created profile
        if not hasattr(farmer_user, 'profile'):
            print("ERROR: Profile not created for farmer_user (Signal failed?)")
            return
        
        farmer_user.profile.role = 'farmer'
        farmer_user.profile.save()
        print("created farmer_bob")
    except Exception as e:
        print(f"ERROR creating farmer: {e}")
        return

    # 2. Add Product
    try:
        product = Product.objects.create(
            farmer=farmer_user,
            name='Test Apple',
            category='fruit',
            price=1.50,
            stock=10,
            description='Fresh apple',
            # image not strictly needed for DB test unless required
            image='products/test.jpg' 
        )
        print("created product Test Apple")
    except Exception as e:
        print(f"ERROR creating product: {e}")
        return

    # 3. Register Customer
    try:
        customer_user = User.objects.create_user(username='customer_alice', email='alice@example.com', password='password123')
        if not hasattr(customer_user, 'profile'):
            print("ERROR: Profile not created for customer_user")
            return
        customer_user.profile.role = 'customer'
        customer_user.profile.save()
        print("created customer_alice")
    except Exception as e:
        print(f"ERROR creating customer: {e}")
        return

    # 4. Place Order (Simulate view logic)
    try:
        # Check logic from orders/views.py
        p = Profile.objects.get(user=customer_user)
        if p.role != 'customer':
            print("ERROR: Customer role check failed")
            return
        
        prod = Product.objects.get(id=product.id)
        if prod.stock <= 0:
            print("ERROR: Stock check failed")
            return
            
        Order.objects.create(
            customer=customer_user,
            product=prod,
            quantity=1
        )
        
        prod.stock -= 1
        prod.save()
        
        print("Order placed successfully!")
    except Exception as e:
        print(f"ERROR placing order: {e}")
        return

    print("--- Test Completed Successfully ---")

if __name__ == '__main__':
    test_flow()
