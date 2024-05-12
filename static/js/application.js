$(document).ready(function () {
    var count = 1;

    // Функция для инициализации Select2
    function initSelect2(selector) {
        $(selector).select2({
            templateResult: function (product) {
                if (!product.id) {
                    return product.text;
                }
                var imageUrl = $(product.element).data('imageUrl');
                return $('<div class="select-product-card"><img src="' + imageUrl +
                    '" class="img-flag" style="height: 50px; width: auto;" />' +
                    '<span>' + product.text + '</span></div>');
            }
        }).on('select2:select', function (e) {
            var selectedOption = e.params.data.element;
            var imageUrl = $(selectedOption).data('imageUrl');
            var id = $(this).attr('id').split('_')[1];
            if (imageUrl) {
                $('#image-preview_' + id).attr('src', imageUrl).show();
            } else {
                $('#image-preview_' + id).hide();
            }
        });
    }
    

    // Инициализация Select2 для первого селекта
    initSelect2('#product_1');

    $(document).on('click', '.add-product', function (e) {
        e.preventDefault();
        count++;
    
        var newSelectId = 'product_' + count;
        var newSelect = $('<select></select>').attr({
            id: newSelectId,
            name: newSelectId,
            class: 'form-control product-card',
            required: 'required'
        });
    
        // Явное копирование каждой опции с данными
        $('#product_1 option').each(function () {
            var option = $('<option></option>').text($(this).text())
                .val($(this).val())
                .data('imageUrl', $(this).data('imageUrl'))
                .data('price', $(this).data('price'));
            newSelect.append(option);
        });

        var product = $('<div>').addClass('product');
        product.append($('<button>').attr({
            type: 'button',
            class: 'delete-product'
        }).append($('<div>').addClass('lnr lnr-cross')));

        product.append($('<h4>').text('Товар ' + count));
        product.append($('<img>').attr({
            id: 'image-preview_' + count,
            src: '',
            style: 'display: none; width: 100px; height: auto;'
        }));

        product.append($('<div>').addClass('row')
            .append($('<div>').addClass('col-lg-6')
                .append($('<div>').addClass('form-group')
                    .append($('<div>').addClass('input-lable')
                        .append($('<label>').attr('for', newSelectId).text('Название товара:'))
                        .append($('<div>').append(newSelect))
                    )
                )
            )
            .append($('<div>').addClass('col-lg-6')
                .append($('<div>').addClass('form-group')
                    .append($('<div>').addClass('input-lable')
                        .append($('<label>').attr('for', 'number_' + count).text('Количество:'))
                        .append($('<div>').addClass('form-holder')
                            .append($('<span>').addClass('lnr lnr-sort-amount-asc'))
                            .append($('<input>').attr({
                                type: 'number',
                                name: 'number_' + count,
                                id: 'number_' + count,
                                class: 'form-control',
                                required: true
                            }))
                        )
                        .append($('<div>').addClass('input-lable')
                            .append($('<label>').attr('for', 'image_' + count).text('Образец продукта')))
                        .append($('<img>').attr({
                                id: 'file-preview_' + count,
                                src: '',
                                style: 'display: none; width: 100px; height: auto; margin-top: 10px;',
                                alt: 'file preview' + count
                            }))
                        .append($('<div>').addClass('form-holder')
                            .append($('<label>').addClass('file-label').attr('for', 'image_' + count).text('Выберите файл'))
                            .append($('<input>').attr({
                                type: 'file',
                                name: 'image_' + count,
                                id: 'image_' + count,
                                class: 'form-control file-input',
                                accept: '.jpg, .png',
                                required: true
                            }))
                        )
                    )
                )
            )
        );

        $('#product-list').append(product);
        initSelect2('#' + newSelectId); // Инициализация Select2 для нового селекта
    });
    $(document).on('click', '.delete-product', function (e) {
        e.preventDefault();
        const product = $(this).closest('.product');
    
        const price = parseFloat(product.find('select option:selected').data('price'));
        const quantity = parseFloat(product.find('input[type=number]').val());
        if (!isNaN(price) && !isNaN(quantity)) {
            const productTotal = price * quantity;
    
            var total = parseFloat($('#total-price').text().replace(' руб.', ''));
            total -= productTotal;
            $('#total-price').text(total.toFixed(2) + ' руб.');
        }
    
        product.remove();
    });
    

    $(document).on('select2:select', 'select[id^="product_"]', function (e) {
        var selectedOption = e.params.data.element;
        var imageUrl = $(selectedOption).data('imageUrl');
        var id = $(this).attr('id').split('_')[1];
        if (imageUrl) {
            $('#image-preview_' + id).attr('src', imageUrl).show();
        } else {
            $('#image-preview_' + id).hide();
        }
    });
    
    

    $(document).on('change', 'input[type="file"]', function () {
        var fileInput = this;
        var id = $(this).attr('id').split('_')[1];
        if (fileInput.files && fileInput.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#file-preview_' + id).attr('src', e.target.result).show();
            };
            reader.readAsDataURL(fileInput.files[0]);
        }
    });

    $(document).on('change', 'select, input[type=number]', function () {
        var total = 0;
        $('.product').each(function () {
            var price = parseFloat($(this).find('select option:selected').data('price'));
            var quantity = parseFloat($(this).find('input[type=number]').val());
            if (!isNaN(price) && !isNaN(quantity)) {
                total += price * quantity;
            }
        });
        $('#total-price').text(total.toFixed(2) + ' руб.');
    });
    // function formatProduct (product) {
    //     if (!product.id) {
    //         return product.text;
    //     }
    //     var imageUrl = product.element.dataset.imageUrl;
    //     var $product = $(
    //     '<div class="select-product-card"><img src="' + imageUrl + '" class="img-flag" style="height: 50px; width: auto;" />' + '<span>' + product.text +  '</span></div>'
    //     );
    //     return $product;
    // };

    // $('#product_1').select2({
    //     templateResult: formatProduct
    // });

});
