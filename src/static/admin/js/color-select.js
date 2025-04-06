/**
 * JavaScript for enhancing color select fields with color swatches
 */
(function($) {
    'use strict';
    
    $(document).ready(function() {
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
        function initColorSelects() {
            // For standalone color selects
            $('select[name="name"]').select2({
                width: '100%',
                templateResult: formatColorOption,
                templateSelection: formatColorOption
            });
            
            // For inline color selects
            $('.inline-group select[name$="-name"]').each(function() {
                $(this).select2({
                    width: '100%',
                    templateResult: formatColorOption,
                    templateSelection: formatColorOption
                });
            });
        }
        
        // Initialize on page load
        initColorSelects();
        
        // Re-initialize when inline forms are added
        $(document).on('formset:added', function() {
            initColorSelects();
        });
    });
})(django.jQuery);
