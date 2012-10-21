$(function () {
    var display_no_flagged_recipes_message = function () {
        $("#flagged_recipes").remove();
        $("#no_flagged_recipes").show();
    };
    
    $(document).on("click", "a.unflag-recipe", function (event) {
        event.preventDefault();
        var $link = $(this);
        $.post($link.attr("href")).always(function (response) {
            $link.closest("li").remove();
            recipe_count = parseInt(response.recipe_count, 10);
            flagging.update_count(recipe_count);
            if (recipe_count === 0) {
                display_no_flagged_recipes_message();
            }
        });
    });
    
    $(document).on("click", "#unflag_all_recipes", function (event) {
        event.preventDefault();
        var is_sure = window.confirm(
            "Are you sure you want to unflag all recipes?"
        );
        
        if (is_sure) {
            $.post($(this).attr("href")).always(function (recipe_count) {
                flagging.update_count(recipe_count);
                display_no_flagged_recipes_message();
            });
        }
    });
});