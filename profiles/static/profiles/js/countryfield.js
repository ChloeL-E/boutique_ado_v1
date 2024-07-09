// code to ensure country field on UserProfile form is grey when no country selected and black when a country is selected

let countrySelected = $('#id_default_country').val();
if(!countrySelected) { // if country selected is false set colour to grey to demo none selected
    $('#id_default_country').css('color', '#aab7c4');
};
$('#id_default_country').change(function() { // capture change event
    countrySelected = $(this).val(); // every time the box changes, get the value of it then determine the proper colour
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});