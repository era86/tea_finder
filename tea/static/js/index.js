function getTeas() {
    var query = $('.filter-query').val();

    var categories = [];
    var caffeines = [];

    $('input[name=caffeine]').each(function(){
        if ($(this).attr('checked')) {
            caffeines.push($(this).val());
        }
    });

    $('input[name=category]').each(function(){
        if ($(this).attr('checked')) {
            categories.push($(this).val());
        }
    });

    $.ajax({
        url: 'teafinder/get_teas',
        data: {
            query: query,
            caffeines: JSON.stringify(caffeines),
            categories: JSON.stringify(categories)
        },
        success: function(d) {
            $('.tea-info-cont').html('');
            $('#tea-table').children().remove();
            $('#tea-row-tmpl').tmpl(d.teas).appendTo('#tea-table');
            $(document).trigger('teafinder.gettea-postload');
        }
    });
}

$(function(){
    getTeas();
});

$(function(){
    $('.filter-query').keyup(function(){
        getTeas();
    });
});

$(function(){
    $('.checkbox-cont input').change(function(){
        getTeas();
    });
});

$(document).bind('teafinder.gettea-postload', function() {
    $('#tea-table tr').click(function(){
        var id = $(this).attr('id');

        $('#tea-table tr').removeClass('tea-selected');
        $(this).addClass('tea-selected');

        $.ajax({
            url: 'teafinder/get_tea',
            data: {
                id: id
            },
            success: function(d) {
                $('.tea-info-cont').html('');
                $('#tea-info-tmpl').tmpl(d).appendTo('.tea-info-cont');
            }
        });

    });
});
