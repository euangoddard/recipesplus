$(function () {
    "use strict";
    
    $(document).on("click", "a.unflag-recipe, a.flag-recipe", function (event) {
        event.preventDefault();
        var $link = $(this);
        $.post($link.attr("href")).always(function (response) {
            $link.replaceWith(response.new_html);
            var recipe_count = response.recipe_count;
            flagging.update_count(recipe_count);
        });
    });
});
