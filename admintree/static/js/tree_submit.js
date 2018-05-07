function submitTree() {
    var json = JSON.stringify($('#nestable1').nestable('serialize'));
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $(".default.save").prop("disabled", true);

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $.ajax({
        type: "POST",
        url: window.location.origin + "/ajax/tree/",
        data: json,
        contentType: "application/json; charset=utf-8",
    }).done(
        function(){
                location.reload();
});
}

$(
    function() {
        $('.dd').nestable('collapseAll');

        $(".ignore").click(function () {
            if ($(this).prop("checked")) {
                $(this).parents("li").attr('data-ignore', true);
            }
            else {
                $(this).parents("li").attr('data-ignore', false);
            }
     });

    $('#nestable-menu').on('click', function(e)
        {
            var target = $(e.target),
                action = target.data('action');
            if (action === 'expand-all') {
                $('.dd').nestable('expandAll');
            }
            if (action === 'collapse-all') {
                $('.dd').nestable('collapseAll');
            }
        });

}
)
