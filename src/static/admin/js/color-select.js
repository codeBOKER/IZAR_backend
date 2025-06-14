/**
 * JavaScript for enhancing color select fields with color swatches
 */
(function($) {
    'use strict';
    
    // Function to format color options with swatches
    function formatColorOption(option) {
        if (!option.id) {
            return option.text;
        }
        
        // Create the color swatch
        var $option = $(
            '<span><span class="color-swatch" style="background-color: #' + 
            option.id + ';"></span>' + option.text + '</span>'
        );
        
        return $option;
    }
    
    // Initialize Select2 for color selects in the admin
    function initColorSelects(context) {
        // context: document or new inline row
        $(context).find('select[name="name"]').select2({
            width: '100%',
            templateResult: formatColorOption,
            templateSelection: formatColorOption
        });
        
        $(context).find('select[name$="-name"]').each(function() {
            $(this).select2({
                width: '100%',
                templateResult: formatColorOption,
                templateSelection: formatColorOption
            });
        });
    }
    
    $(document).ready(function() {
        // Initialize on page load
        initColorSelects(document);
        
        // Re-initialize when inline forms are added
        $(document).on('formset:added', function(event, $row) {
            initColorSelects($row);
        });
    });
})(django.jQuery);
