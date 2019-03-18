(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict

$(".asignar-dir").click(function() {
  var $row = $(this).closest("tr")   // Finds the closest row <tr>

  $('input[name=NewDirFlag]').val("False");

  $('input[name=idDir]').val($row.find("td:nth-child(1)").text().trim());
  $('input[name=tipo_via]').val($row.find("td:nth-child(2)").text().trim());
  $('input[name=nombre_via]').val($row.find("td:nth-child(3)").text().trim());
  $('input[name=nro_via]').val($row.find("td:nth-child(4)").text().trim());
  $('input[name=portalescalotros_via]').val($row.find("td:nth-child(5)").text().trim());
  $('input[name=cp_via]').val($row.find("td:nth-child(6)").text().trim());
  $('input[name=ciudad_via]').val($row.find("td:nth-child(7)").text().trim());
  $('input[name=provincia_via]').val($row.find("td:nth-child(8)").text().trim());
  $('input[name=pais_via]').val($row.find("td:nth-child(9)").text().trim());

});

$(".crear-nueva-dir").click(function() {

  $('input[name=NewDirFlag]').val("True");

  $('input[name=idDir]').val('');
  $('input[name=tipo_via]').val('');
  $('input[name=nombre_via]').val('');
  $('input[name=nro_via]').val('');
  $('input[name=portalescalotros_via]').val('');
  $('input[name=cp_via]').val('');
  $('input[name=ciudad_via]').val('');
  $('input[name=provincia_via]').val('');
  $('input[name=pais_via]').val('');
});