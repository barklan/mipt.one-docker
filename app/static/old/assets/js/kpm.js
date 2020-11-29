$("#kpm").bind("load", function () { $(this).fadeIn(1000); });

/*
var downloadingImage = new Image();
downloadingImage.src = "/images/background.jpg";
*/
$('body').ready(function() { 
    $('#kpm').each(function(i) {
            if (this.complete) {
                $(this).fadeIn();
            } else {
                $(this).load(function() {
                    $(this).fadeIn(1500);
                });
            }
        });
    });