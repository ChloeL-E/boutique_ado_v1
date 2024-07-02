/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1); /* get the script elements text and slice off the quotation marks */
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey); /* made poss by the stripe js in the base template- make a variable containing the stripe public key */
var elements = stripe.elements(); /* create an instance of the stripe elements */
var style = { /* style the card element using the stripe css, ensure styling is before the create card element */ 
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
card.mount('#card-element'); /* mount the card to the #card-element div */

// Handle realtime validation errors on the card element- displays error message if card details incorrect
// stripe works with paymentsIntents. When user hits the checkout page, the checkout view creates a stripe paymentIntent
// stripe returns client_secret, which we return to the template as the client secret variable
// in the js on the client side we call the confirmCardPayment() method from stripe js using the client secret which will verify the card number
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true}); // disable to prevent multiple submissions
    $('#submit-button').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, { // call the confirmCardPayment method to send the details securely to stripe
        payment_method: { 
            card: card, // provide the card to stripe
        }
    }).then(function(result) { // then execute this function on the result
        if (result.error) { // if an error put the message stright into the card-error div
            // show error to your customer(e.g. insufficient funds)
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({ 'disabled': false}); // if theres a card error we want to reenable the submit button so the user can fix it
            $('#submit-button').attr('disabled', false);
        } else { 
            // the payment has been processed
            if (result.paymentIntent.status === 'succeeded') {
                form.submit(); // if the card details come back that they have succeeded we'll submit the form
            }
        }
    });
});