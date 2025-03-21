$(document).ready(function() {
    // Handle quantity decrease button
    $('.btn-minus').on('click', function() {
        const input = $(this).closest('.quantity').find('input');
        const cartId = $(this).closest('tr').data('cart-id');
        let value = parseInt(input.val());
        
        if (value > 1) {
            value = value - 1;
            input.val(value);
            updateItemQuantity(cartId, value);
        }
    });
    
    // Handle quantity increase button
    $('.btn-plus').on('click', function() {
        const input = $(this).closest('.quantity').find('input');
        const cartId = $(this).closest('tr').data('cart-id');
        let value = parseInt(input.val());
        
        value = value + 1;
        input.val(value);
        updateItemQuantity(cartId, value);
    });
    
    // Handle direct input change
    $('.quantity input').on('change', function() {
        const cartId = $(this).closest('tr').data('cart-id');
        let value = parseInt($(this).val());
        
        // Ensure quantity is at least 1
        if (isNaN(value) || value < 1) {
            value = 1;
            $(this).val(value);
        }
        
        updateItemQuantity(cartId, value);
    });
    
    // Handle remove button
    $('.btn-danger').on('click', function() {
        const cartId = $(this).closest('tr').data('cart-id');
        removeCartItem(cartId);
    });
    
    // Function to update item quantity via AJAX
    function updateItemQuantity(cartId, quantity) {
        $.ajax({
            url: '/update_cart_quantity',
            type: 'POST',
            data: {
                cart_id: cartId,
                quantity: quantity
            },
            success: function(response) {
                if (response.success) {
                    // Update item total price
                    $(`tr[data-cart-id="${cartId}"]`).find('.item-total').text('$' + response.item_total.toFixed(2));
                    
                    // Update cart summary
                    updateCartSummaryValues(response.subtotal, response.shipping, response.total);
                } else {
                    console.error('Error updating quantity:', response.error);
                    alert('Failed to update quantity: ' + response.error);
                }
            },
            error: function(xhr) {
                console.error('Error updating quantity:', xhr.responseText);
                alert('Failed to update quantity. Please try again.');
            }
        });
    }
    
    // Function to remove cart item via AJAX
    function removeCartItem(cartId) {
        $.ajax({
            url: '/remove_from_cart',
            type: 'POST',
            data: {
                cart_id: cartId
            },
            success: function(response) {
                if (response.success) {
                    // Remove the item row from the table
                    $(`tr[data-cart-id="${cartId}"]`).remove();
                    
                    // Update cart summary
                    updateCartSummaryValues(response.subtotal, response.shipping, response.total);
                    
                    // If cart is now empty, reload the page to show empty cart message
                    if (response.subtotal === 0) {
                        location.reload();
                    }
                } else {
                    console.error('Error removing item:', response.error);
                    alert('Failed to remove item: ' + response.error);
                }
            },
            error: function(xhr) {
                console.error('Error removing item:', xhr.responseText);
                alert('Failed to remove item. Please try again.');
            }
        });
    }
    
    // Update the cart summary display
    function updateCartSummaryValues(subtotal, shipping, total) {
        $('.cart-subtotal').text('$' + subtotal.toFixed(2));
        $('.cart-shipping').text('$' + shipping.toFixed(2));
        $('.cart-total').text('$' + total.toFixed(2));
        
        // Also update checkout button state
        if (subtotal === 0) {
            $('.btn-primary.my-3').prop('disabled', true);
        } else {
            $('.btn-primary.my-3').prop('disabled', false);
        }
    }
});