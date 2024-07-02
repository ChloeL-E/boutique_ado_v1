/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1); /* get the script elements text and slice off the quotation marks */
var client_secret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key); /* made poss by the stripe js in the base template- make a variable containing the stripe public key */
var elements = stripe.elements(); /* create an instance of the stripe elements */
var style = { /* style the card element using the stripe css*/ 
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style}); /* create a card element */
card.mount('#card-element'); /* moutnt he card element to the #card-element div */