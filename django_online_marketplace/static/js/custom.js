











$(document).ready(function(){
    $('.add_to_cart').on('click',function(e) {
        e.preventDefault();

        product_id = $(this).attr('data-id');
        url = $(this).attr('data-id');

        data = {
            product_id:product_id,
        }

        $.ajax({
            type: 'GET',
            url:url,
            data: data,
            success: function(response){
                alert(response)
            }
        })
    })


    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#' + the_id).html(qty)
    })
});
