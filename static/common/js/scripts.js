jQuery(document).ready(function() {

    /*
        Background slideshow
    */
    $.backstretch([
      "static/images/backgrounds/1.jpg"
    , "static/images/backgrounds/2.jpg"
    , "static/images/backgrounds/3.jpg"
    ], {duration: 3000, fade: 750});

    /*
        Tooltips
    */
    $('.links a.home').tooltip();
    $('.links a.blog').tooltip();

});
