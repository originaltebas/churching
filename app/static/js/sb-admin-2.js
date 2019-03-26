(function ($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function (e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function () {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function (e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function () {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function (e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict

$(".asignar-dir").click(function () {
  var $row = $(this).closest("tr") // Finds the closest row <tr>

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

$(".crear-nueva-dir").click(function () {

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


$(".agregar-quitar-miembros").click(function () {
  // Uso la misma accion asociada a los dos y uso el tag-accion para
  // saber si tengo que quitar o agregar miembro
  // If -> quitar -> else -> agregar
  if ($(this).attr("tag-accion") == "quitar") {
    // Cambio el flag de modificacion a True
    $('input[name=modifFlag]').val("True");

    // cojo el id del miembro quitado para eliminarlo de la lista de
    // los miembros del grupo
    var idquitar = $(this).attr('tag-id');
    // cojo los ids de los miembros del grupo
    var ids = $('input[name=ids]').val();
    // quito el id del miembro a quitar de la lista total de miembros
    ids = ids.replace(idquitar + ",", "");

    // Lo mismo para totales
    var idagregar = $(this).attr('tag-id');
    var ids_t = $('input[name=ids_totales]').val();
    ids_t = ids_t + idagregar + ",";

    // Si la lista total de miembros del grupo esta vacia
    // quito la clase de ocultar para que se vea la fila "no hay miembros"
    // sino la pongo
    if (ids == "") {
      $(".tag-coletilla-ma").removeClass("d-none");
    } else {
      $(".tag-coletilla-ma").addClass("d-none");
    }
    // modifico el campo hidden del form que mantiene la lista de miembros
    $('input[name=ids]').val(ids);
    $('input[name=ids_totales]').val(ids_t);

    // Pongo el contador de cantidad de grupos a 0 para el miembro quitado
    $(this).closest("tr").children(".count-in").text("0");
    // Cambio el texto de quitar a agregar
    $(this).text("Agregar");
    //cambio la etiqueta de accion a agregar (tenía quitar)
    $(this).attr("tag-accion", "agregar");

    // Muevo fila de la tabla incluidos a la tabla no incluidos
    var whichtr = $(this).closest("tr");
    $('.m-no-incluidos').append(whichtr);

    // Resto 1 a la cuenta de miembros del grupo casero
    var min = (parseInt($('.count-gc').text()) - 1);
    $('.count-gc').text(min);

    $(".tag-coletilla-mni").addClass("d-none");

    // accion agregar
  } else {
    // Cambio el flag de modificacion a True
    $('input[name=modifFlag]').val("True");

    // cojo el id del miembro agregado para sumarlo de la lista de
    // los miembros del grupo
    var idagregar = $(this).attr('tag-id');
    // cojo los ids de los miembros del grupo
    var ids = $('input[name=ids]').val();
    // sumo el id del miembro a lista total de miembros
    ids = ids + idagregar + ",";

    // Lo mismo para totales
    var idquitar = $(this).attr('tag-id');
    // cojo los ids de los miembros del grupo
    var ids_t = $('input[name=ids_totales]').val();
    // quito el id del miembro a quitar de la lista total de miembros
    ids_t = ids_t.replace(idquitar + ",", "");

    // Si la lista total de miembros del grupo esta vacia
    // quito la clase de ocultar para que se vea la fila "no hay miembros"
    // sino la pongo
    if (ids_t == "") {
      $(".tag-coletilla-mni").removeClass("d-none");
    } else {
      $(".tag-coletilla-mni").addClass("d-none");
    }
    // modifico el campo hidden del form que mantiene la lista de miembros
    $('input[name=ids]').val(ids);
    $('input[name=ids_totales]').val(ids_t);

    // Pongo el contador de cantidad de grupos a 1 para el miembro sumado
    $(this).closest("tr").children(".count-in").text("1");
    // Cambio el texto del boton
    $(this).text("Quitar");
    //cambio la etiqueta de accion a quitar (tenía agregar)
    $(this).attr("tag-accion", "quitar");

    // Muevo fila de la tabla incluidos a la tabla no incluidos
    var whichtr = $(this).closest("tr");
    $('.m-incluidos').append(whichtr);

    // Resto 1 a la cuenta de miembros del grupo casero
    var min = (parseInt($('.count-gc').text()) + 1);
    $('.count-gc').text(min);

    $(".tag-coletilla-ma").addClass("d-none");
  }
});

$('#ndir').on('click', function () {
  $('.modal-content').load('crear/nuevadir/loadForm', function () {
    $('#myModal').modal({
      show: true,
      closable: false,
      transition: 'fade up',
    });
  });
});

$('#udir').on('click', function () {
  $('.modal-content').load('crear/usardir/loadForm', function () {
    $('#myModal').modal({
      show: true,
      closable: false,
      transition: 'fade up',
    });
  });
});

function after_form_submitted(data) {
  if (data.status == 'ok') {
    $('input[name=idDir]').val(data.id);
    $("#cardBodyButtons").removeClass("d-none");
    $('#cardBodyDir').load('crear/loadDir/' + data.id);
    $('#myModal').modal('hide');
  } else {
    $('#myModal .modal-content').html(data);
    return false;
  }
}

function after_form_submitted_f(data) {
  window.location.href = data.url;
}

$(document).on('click', '#btnCrear', function (e) {
  e.preventDefault();
  url = 'crear/nuevadir'
  $.ajax({
    type: "POST",
    url: url,
    data: $('#nDirForm').serialize(),
    success: after_form_submitted,
    dataType: 'json'
  });
})

$(document).on('click', '#btnCrearFam', function (e) {
  e.preventDefault();
  url = 'crear'
  $.ajax({
    type: "POST",
    url: url,
    data: $('#familyForm').serialize(),
    success: after_form_submitted_f,
    dataType: 'json'
  });
})