(function ($) {
    "use strict";
    
    var INGREDIENT_TEMPLATE = Handlebars.compile(
        '<input type="text" class="input-xxlarge ingredient{{#if is_heading }} heading{{/if}}" placeholder="Add ingredient" value="{{ ingredient }}">'
    );
    
    var RETURN_KEYS = [$.ui.keyCode.ENTER, $.ui.keyCode.NUMPAD_ENTER];
    
    var INGREDIENT_SELECTOR = "input.ingredient";
    
    var HEADING_CLASS = "heading";
    
    $.widget("ui.ingredients_widget", {
        _create: function () {
            this.element.hide();
            this.parent_element = this.element.parent();
            this.control_panel = $("#ingredients-control-panel");
            this.heading_control = this.control_panel.find('[name="is_heading"]');
            this.current_editing_element = null;
            this._setup_events();
            this._parse_original();
        },
        
        _parse_original: function () {
            var widget = this;
            var raw_ingredients = $.parseJSON(this.element.val());
            
            if (!raw_ingredients.length) {
                raw_ingredients = [''];
            }
            
            $.each(raw_ingredients, function () {
                widget._add_ingredient(this.text, this.heading);
            });
            
        },
        
        _sync_original: function () {
            var ingredient_data = [];
            this.parent_element.find(INGREDIENT_SELECTOR).each(function () {
                var $ingredient = $(this);
                ingredient_data.push({
                    text: $ingredient.val(),
                    heading: $ingredient.hasClass(HEADING_CLASS)
                });
            });
            this.element.val(JSON.stringify(ingredient_data));
        },
        
        _setup_events: function () {
            var self = this;
            this.parent_element.on("focus", INGREDIENT_SELECTOR, function () {
                var $ingredient_item = $(this);
                var ingredient_item_offset = $ingredient_item.offset();
                self.current_editing_element = $ingredient_item;
                setTimeout(function () {
                    self.heading_control.prop(
                        "checked",
                        $ingredient_item.hasClass(HEADING_CLASS)
                    );
                    self.control_panel.css({
                        top: ingredient_item_offset.top + "px",
                        left: ingredient_item_offset.left + $ingredient_item.outerWidth() + "px"
                    }).show();
                }, 100);
            }).on("blur", INGREDIENT_SELECTOR, function () {
                self.current_editing_element = null;
                self.control_panel.hide();
            }).on("keypress", INGREDIENT_SELECTOR, function (evt) {
                if (!evt.shiftKey && $.inArray(evt.keyCode, RETURN_KEYS) !== -1) {
                    var $ingredient = $(this);
                    evt.preventDefault();
                    var $next_ingredient = $ingredient.next(INGREDIENT_SELECTOR);
                    if ($next_ingredient.length) {
                        $next_ingredient.trigger("focus");
                    } else {
                        self._insert_ingredient($ingredient);
                        setTimeout(function () {
                            $ingredient.next(INGREDIENT_SELECTOR).trigger("focus");
                        }, 50);
                    }
                }
            }).on("keyup", INGREDIENT_SELECTOR, function (evt) {
                if (evt.keyCode === $.ui.keyCode.BACKSPACE) {
                    var $ingredient = $(this);
                    var $previous_ingredient = $ingredient.prev(INGREDIENT_SELECTOR);
                    if ($ingredient.val() === "" && $previous_ingredient.length) {
                        self._remove_ingredient($ingredient);
                        $previous_ingredient.focus();
                    }
                }
            });
            
            this.parent_element.closest("form").on("submit", function () {
                self._sync_original();
            });
            
            this.control_panel.on("mousedown", "a", function (evt) {
                evt.preventDefault();
                var action = $(this).data("action");
                var method_name = "_" + action + "_ingredient";
                var method = self[method_name];
                if (method) {
                    method.call(self, self.current_editing_element);
                }
            }).on("mousedown", ":checkbox, label", function (evt) {
                evt.preventDefault();
                evt.stopPropagation();
                self._toggle_heading_state(self.current_editing_element);
            });
        },
        
        _add_ingredient: function (text, is_heading, $insert_after) {
            var ingredient_html = INGREDIENT_TEMPLATE({
                ingredient: text,
                is_heading: is_heading
            });
            
            if ($insert_after) {
                $insert_after.after(ingredient_html);
            } else {
                this.parent_element.append(ingredient_html);
            }
        },
        
        _remove_ingredient: function (ingredient) {
            ingredient.remove();
        },
        
        _insert_ingredient: function (after_ingredient) {
            this._add_ingredient("", false, after_ingredient);
        },
        
        _toggle_heading_state: function (ingredient) {
            ingredient.toggleClass(HEADING_CLASS);
        }
        
    });
    
    $(function () {
        $(".ingredients-widget").ingredients_widget();
    });
    
})(jQuery);
