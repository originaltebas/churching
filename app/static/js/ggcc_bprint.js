function ggccElements(e) {

  // GGCC -> Listado de grupos caseros
  if ($('#tbListarGGCC').length != 0) {
    $(tbListarGGCC).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      }
    });
  }

  // FUNCIONALIDADES DE CREAR GRUPO CASERO
  if ($('#tbCrearGC').length != 0) {
    /**
     * Par de funciones para Crear (Guardar) datos Grupo Casero
     *  */
    function after_ggcc_submitted(data) {
      window.location.href = data.url;
    }

    $(document).on('click', '#btnCrearGC', function (e) {
      e.preventDefault();
      url = '/ggcc/crear'
      $.ajax({
        type: "POST",
        url: url,
        data: $('#tbCrearGC').serialize(),
        success: after_ggcc_submitted,
        dataType: 'json'
      });
    })
  }
  /*
  * Fin Par funciones Modificar GC
  */

  // FUNCIONALIDADES DE CREAR GRUPO CASERO
  if ($('#tbModificarGC').length != 0) {
    /**
     * Par de funciones para Modificar (Guardar) datos Grupo Casero
     *  */
    function after_ggcc_submitted(data) {
      window.location.href = data.url;
    }

    $(document).on('click', '#btnModificarGC', function (e) {
      e.preventDefault();
      id = $('#id').val();
      url = '/ggcc/modificar/' + id
      $.ajax({
        type: "POST",
        url: url,
        data: $('#tbModificarGC').serialize(),
        success: after_ggcc_submitted,
        dataType: 'json'
      });
    })
  }
  /**
  * Fin Par funciones Modificar GC
  */



  /**
   * Funciones comunes a Crear, Modificar y Asignar
   * por lo que se ponen disponibles para todos
   */

  // Boton Crear Nueva Direccion
  $(document).on('click', '#nuevaDireccion', function (e) {
    $('.modal-content').load('/direcciones/loadFormNueva', function () {
      $('#myModal').modal({
        show: true,
        closable: false,
        transition: 'fade up',
      });
    });
  });

  // Boton Usar Direccion Existente
  $(document).on('click', '#usarDireccion', function (e) {
    $('.modal-content').load('/direcciones/loadFormUsar', function () {
      $('#myModal').modal({
        show: true,
        closable: false,
        transition: 'fade up',
      });
    });
  });

  // Ajustar la ventana del modal al tamaño de las tablas
  $(document).on('shown.bs.modal', "#myModal", function (e) {
    $(this).find('.modal-dialog').css({
      width: 'auto',
      height: 'auto',
      'max-height': '70%',
      'max-width': '70%',
    });
  });

  // Link de pasar pagina de la lista de direcciones.
  // Coje el url y lo lanza de nuevo al modal
  $(document).on('click', '.page-link', function (e) {
    e.preventDefault();
    var url = $(this).attr("href");
    $('.modal-content').load(url, function () {
      $('#myModal').modal({
        show: true,
        closable: false,
        transition: 'fade up',
      });
    });
  });

  // Asigna la direccion desde el modal (lo cierra) y aparece en la pantalla principal de gc, familia o mb
  $(document).on("click", ".asignar-dir", function (e) {
    var $row = $(this).closest("tr"); // Finds the closest row <tr>
    var id_direccion_elegida = $row.find("td:nth-child(1)").text().trim();

    // asigna el id de direccion a la variable oculta id_direccion
    $('input[name=id_direccion]').val(id_direccion_elegida);
    $("#cardBodyButtons").removeClass("d-none");
    $('#cardBodyDir').load('/direcciones/loadDir/' + id_direccion_elegida);
    $('#myModal').modal('hide');
  })

  /**
   * Par de funciones para Crear Direccion en el Modal
   * Sirve tanto para Crear grupo casero como para modificarlo
   */
  function after_nueva_direccion_submitted(data) {
    //Si el formulario se guarda bien
    if (data.status == 'ok') {
      $('input[name=id_direccion]').val(data.id);
      $("#cardBodyButtons").removeClass("d-none");
      $('#cardBodyDir').load('/direcciones/loadDir/' + data.id);
      $('#myModal').modal('hide');
    } else if (data.status == 'v_error') {  //funcion para marcar los campos invalidos en el formulario
        $("form#nDirForm :input").each(function(){
          $(this).removeClass("is-invalid");
        });
        data.errores.forEach(function (value, key) {
          $('#' + value).addClass("is-invalid");
        });
        return false;
    } else {
        return false;
    }
  }

  $(document).on('click', '#btnCrearDireccion', function (e) {
    e.preventDefault();
    url = '/direcciones/creardireccion'
    $.ajax({
      type: "POST",
      url: url,
      data: $('#nDirForm').serialize(),
      success: after_nueva_direccion_submitted,
      dataType: 'json'
    });
  })

  // Esta funcion limpia el formulario modal de los campos inválidos
  // a medida que se rellenan los datos.
  $(document).on('focus', "form#nDirForm .form-control-user", function(e) {
      $(this).removeClass('is-invalid');
  });

  /**
   * Fin par funciones para crear direccion
   */

}
window.addEventListener("load", ggccElements, false);
