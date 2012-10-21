var alerts = alerts || {};

(function (module) {
    "use strict";
    module.init = function () {
        $(function () {
            $(document).on("click", ".alert button.close", function () {
                $(this).closest(".alert").remove();
            });
        });
    }
})(alerts);

alerts.init();


var flagging = flagging || {};

(function (module) {
    
    var ACTIVE_FLAGGED_RECIPES_CLASS = "badge-success";
    
    flagging.update_count = function (new_count) {
        var $dropdown = $("#flagged_recipes_dropdown");
        var repopulation_url = $dropdown.data("repopulation-url");
        $dropdown.load(repopulation_url);
        
        var $flagged_recipe_count = $("#flagged_recipe_count");
        $flagged_recipe_count.text(new_count);
        
        if (new_count === 0) {
            $flagged_recipe_count.removeClass(ACTIVE_FLAGGED_RECIPES_CLASS);
        } else {
            $flagged_recipe_count.addClass(ACTIVE_FLAGGED_RECIPES_CLASS);
        }
    };
})(flagging);


$(function () {
    $(document).on("click", ".dropdown-toggle", function (event) {
        event.preventDefault();
        event.stopPropagation();
        $(this).closest(".dropdown").toggleClass("open");
    });
    
    $(document).on("click", "#flagged_recipes_dropdown", function (event) {
        event.stopPropagation();
    });
    
    $(document).on("click", function (event) {
        $(".dropdown").removeClass("open");
    });
});
