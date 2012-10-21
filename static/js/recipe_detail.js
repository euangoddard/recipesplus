$(function () {
    var change_flag_state = function ($link, $converse_link) {
        $link.prop("disabled", true).addClass("disabled");
        $.post($link.attr("href")).always(function (response) {
            $link.hide();
            $converse_link.removeProp("disabled").removeClass("disabled").show();
            flagging.update_count(response.recipe_count);
        });
    };
    
    $(document).on("click", "#flag_recipe", function (event) {
        event.preventDefault();
        var $link = $(this);
        var $converse_link = $("#unflag_recipe");
        change_flag_state($link, $converse_link);
    });
    
    $(document).on("click", "#unflag_recipe", function (event) {
        event.preventDefault();
        var $link = $(this);
        var $converse_link = $("#flag_recipe");
        change_flag_state($link, $converse_link);
    });
});