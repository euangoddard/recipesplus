(function ($) {
    "use strict";
    
    var INSTRUCTION_TEMPLATE = Handlebars.compile(
        '<textarea class="input-xxlarge instruction" placeholder="Add instruction">{{ instruction }}</textarea>'
    );
    
    var INSTRUCTION_SELECTOR = "textarea.instruction";
    
    $.widget("ui.method_widget", {
        _create: function () {
            this.element.hide();
            this.parent_element = this.element.parent();
            this.control_panel = $("#method-control-panel");
            this.current_editing_element = null;
            this._setup_events();
            this._parse_original();
        },
        
        _parse_original: function () {
            var widget = this;
            
            var lines = this.element.val().split("\n");
            $.each(lines, function () {
                widget._add_instruction(this);
            });
        },
        
        _sync_original: function () {
            var instruction_texts = [];
            this.parent_element.find(INSTRUCTION_SELECTOR).each(function () {
                instruction_texts.push($(this).val());
            });
            this.element.val(instruction_texts.join("\n"));
        },
        
        _setup_events: function () {
            var self = this;
            this.parent_element.on("focus", INSTRUCTION_SELECTOR, function () {
                var $method_item = $(this);
                var method_item_offset = $method_item.offset();
                self.current_editing_element = $method_item;
                setTimeout(function () {
                    self.control_panel.css({
                        top: method_item_offset.top + "px",
                        left: method_item_offset.left + $method_item.outerWidth() + "px"
                    }).show();
                }, 100);
            }).on("blur", INSTRUCTION_SELECTOR, function () {
                self.current_editing_element = null;
                self.control_panel.hide();
            }).on("keypress", INSTRUCTION_SELECTOR, function (evt) {
                if (!evt.shiftKey && evt.keyCode === $.ui.keyCode.ENTER) {
                    var $instruction = $(this);
                    evt.preventDefault();
                    var $next_instruction = $instruction.next(INSTRUCTION_SELECTOR);
                    if ($next_instruction.length) {
                        $next_instruction.trigger("focus");
                    } else {
                        self._insert_instruction($instruction);
                        setTimeout(function () {
                            $instruction.next(INSTRUCTION_SELECTOR).trigger("focus");
                        }, 50);
                    }
                }
            }).on("keyup", INSTRUCTION_SELECTOR, function (evt) {
                if (evt.keyCode === $.ui.keyCode.BACKSPACE) {
                    var $instruction = $(this);
                    var $previous_instruction = $instruction.prev(INSTRUCTION_SELECTOR);
                    if ($instruction.val() === "" && $previous_instruction.length) {
                        self._remove_instruction($instruction);
                        $previous_instruction.focus();
                    }
                }
            });
            
            this.parent_element.closest("form").on("submit", function () {
                self._sync_original();
            });
            
            this.control_panel.on("mousedown", "a", function (evt) {
                evt.preventDefault();
                var action = $(this).data("action");
                var method_name = "_" + action + "_instruction";
                var method = self[method_name];
                if (method) {
                    method.call(self, self.current_editing_element);
                }
            });
        },
        
        _add_instruction: function (instruction_text, $insert_after) {
            var instruction_html = INSTRUCTION_TEMPLATE({
                instruction: instruction_text
            });
            
            if ($insert_after) {
                $insert_after.after(instruction_html);
            } else {
                this.parent_element.append(instruction_html);
            }
        },
        
        _remove_instruction: function (instruction) {
            instruction.remove();
        },
        
        _insert_instruction: function (after_instruction) {
            this._add_instruction("", after_instruction);
        }
    });
    
    $(function () {
        $(".method-widget").method_widget();
    });
    
})(jQuery);