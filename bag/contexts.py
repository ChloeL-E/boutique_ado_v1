from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    ''' 
    Returns a dictionary called context that is available to all apps in project. 
    'bag.contexts.bag_contents' in settings.py>templates>context processors. Means this can be accessed from any template in the project
    '''

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        if isinstance(item_data, int): # Check if item_data is an Integer: This checks if the value associated with item_id is an integer. If it is, it indicates the item does not have different sizes.
            product = get_object_or_404(Product, pk=item_id) # Retrieve Product: get_object_or_404(Product, pk=item_id) fetches the product from the database using the item_id. If the product doesn't exist, it raises a 404 error.
            total += item_data * product.price # Calculate Total Price: The total price is updated by adding the quantity of the item times its price.
            product_count += item_data # Update Product Count: The total count of products is incremented by the quantity of this item.
            bag_items.append({ # Append to Bag Items: A dictionary containing the item_id, quantity, and product is appended to the bag_items list.
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else: # handles items that have sizes (i.e., item_data is a dictionary).
            product = get_object_or_404(Product, pk=item_id) # Retrieve Product: it fetches the product object using the item_id or if none exists an error message.
            for size, quantity in item_data['items_by_size'].items(): # Loop through Sizes: The inner loop iterates over each size and its corresponding quantity in the items_by_size dictionary.
                total += quantity * product.price # Calculate Total Price: For each size, it updates the total by adding the quantity x the product's price.
                product_count += quantity # Update Product Count: It increments the product_count by the quantity for each size
                bag_items.append({ # Append to Bag Items: It appends a dictionary containing the item_id, quantity, product, and size to the bag_items list.
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context