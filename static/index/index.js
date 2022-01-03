$(document).ready(function(){       
    var scroll_start = 0;
    var startchange = $('.navbar');
    var offset = startchange.offset();
    if (startchange.length){
        $(document).scroll(function() { 
        scroll_start = $(this).scrollTop();
        if(scroll_start > offset.top) {
            $(".navbar").removeClass("navbar-light")
            $(".navbar").addClass("navbar-dark")
            $(".navbar").removeClass("bg-light")
            $(".navbar").addClass("bg-dark")
            } else {
                $(".navbar").addClass("navbar-light")
                $(".navbar").removeClass("navbar-dark")
                $(".navbar").addClass("bg-light")
                $(".navbar").removeClass("bg-dark")
            }
        });
    }
 });