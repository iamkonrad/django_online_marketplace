




$(document).ready(function () {
    // Add to cart
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();
        var product_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if (response.status === 'Failed') {
                    console.log('Raise the error message');
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + product_id).html(response.qty);
                }
            }
        });
    });

    // Set item quantities
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#' + the_id).html(qty);
    });

    // Decrease cart
    $('.decrease_cart').on('click', function (e) {
        e.preventDefault();
        var product_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response);
                if (response.status === 'Failed') {
                    console.log(response);
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + product_id).html(response.qty);
                }
            }
        });
    });
});
