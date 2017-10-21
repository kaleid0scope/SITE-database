


(function ($) {
    "use strict";
    var mainApp = {
        scrollAnimation_fun: function () {

            /*====================================
             ON SCROLL ANIMATION SCRIPTS 
            ======================================*/


            window.scrollReveal = new scrollReveal();

        },
        slide_fun: function () {

            /*====================================
             SLIDE  SCRIPTS 
            ======================================*/
           
            $('.carousel').carousel({
                interval: 3000 //TIME IN MILLI SECONDS
            });

        },
        scroll_fun: function () {

            /*====================================
                 SCROLL SCRIPTS 
                ======================================*/
            $(document).ready(function () {
                $('a').smoothScroll();
                $('#nav a').tooltip({
                    container: "body"
                });
            });

        },

      
        custom_fun:function()
        {
            /*====================================
               WOW SCRIPTS 
              ======================================*/
            new WOW().init();
            

            /*====================================
             WRITE YOUR   SCRIPTS  BELOW
            ======================================*/




        },

    }
   
   
    $(document).ready(function () {
        mainApp.scrollAnimation_fun();
        mainApp.slide_fun();
        mainApp.scroll_fun();
        mainApp.custom_fun();
    });
}(jQuery));


