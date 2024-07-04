from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json # from python
import time # from python


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object  
        pid = intent.id # patient intent id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info # user meta data from save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details # updated - store the billing details
        shipping_details = intent.shipping # store the shipping details
        grand_total = round(stripe_charge.amount / 100, 2) # updated - tore the grand total

        # Clean data in the shipping details
        for field, value in shipping_details.address.items(): # to ensure the data is in the same form as in the datatabase
            if value == "": # replace the empty strings in the shipping details with None as stripe with store them as strings rather than the Null values in the database
                shipping_details.address[field] = None

        order_exists = False # if the order doesnt exist...
        attempt = 1 # try to get the order using all the info from the payment intent
        while attempt <= 5: # the webhooks relies on the view creating the order straight away, but what if the view is a little slow to create? instead ofwebhooks then immediately creating the order itself if not found the first time.
            try: # try to get the order 5 times
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name, # case insensitive
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country, # coutnry to county within an address key
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag, # to match on original bag and strip pid...this can help if customer has made the exact same order before 
                    stripe_pid=pid,
                )
                order_exists = True # if the order is found
                break # break out the while loop if order found
            except Order.DoesNotExist:
                attempt += 1 # increment the attempt by 1
                time.sleep(1) # sleep for one second- causes webhook handler to try to find the order 5 times over 5 seconds before giving up and creating the order itself
        if order_exists:
            return HttpResponse( # success response as order found by webhook handler
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None # order not found by webhooks handler, create the order
            try: 
                order = Order.objects.create( # create form to save using the data in the payment intent
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items(): # load from the json bag rather than the session
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete() # if anything goes wrong, delete the order if it was created and send 500 error response
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500) # stripe can then retry the webhook later
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)