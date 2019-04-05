(function ($) {
  "use strict"; // Start of use strict

function botonesDireccion() {
    $('#ndir').on('click', function () {
      $('.modal-content').load('../nuevadir/loadForm', function () {
        $('#myModal').modal({
          show: true,
          closable: false,
          transition: 'fade up',
        });
      });
    });

    $('#udir').on('click', function () {
      $('.modal-content').load('../usardir/loadForm', function () {
        $('#myModal').modal({
          show: true,
          closable: false,
          transition: 'fade up',
        });
      });
    });

    $('#mdira').on('click', function (e) {
        e.preventDefault();
        if (confirm("Si cambias la dirección actual, se modificará"
                     + "en todos los elementos asociados (miembros, ggcc"
                     + "y familias). ¿Estás seguro?")) {
            $('input[name=tipo_via]').prop('readonly', false);
            $('input[name=nombre_via]').prop('readonly', false);
            $('input[name=nro_via]').prop('readonly', false);
            $('input[name=portalescalotros_via]').prop('readonly', false);
            $('input[name=piso_nroletra_via]').prop('readonly', false);
            $('input[name=cp_via]').prop('readonly', false);
            $('input[name=ciudad_via]').prop('readonly', false);
            $('input[name=provincia_via]').prop('readonly', false);
            $('input[name=pais_via]').prop('readonly', false);

            $("#rowModButtonsDir").removeClass("d-none");
            $("#rowButtonsDir").addClass("d-none");

        }
    });

    function after_direccion_actualizda(data) {
        if (data.status=='ok'){
            alert("Datos de dirección actualizados");
        } else {
            alert("Error. Datos de dirección NO actualizados");
        }
    }

    $('#mdiraGuardar').on('click', function (e) {
        e.preventDefault();

        let url = 'actualizarDir/' + $('input[name=idDir]').val();

        $('input[name=tipo_via]').prop('readonly', true);
        $('input[name=nombre_via]').prop('readonly', true);
        $('input[name=nro_via]').prop('readonly', true);
        $('input[name=portalescalotros_via]').prop('readonly', true);
        $('input[name=piso_nroletra_via]').prop('readonly', true);
        $('input[name=cp_via]').prop('readonly', true);
        $('input[name=ciudad_via]').prop('readonly', true);
        $('input[name=provincia_via]').prop('readonly', true);
        $('input[name=pais_via]').prop('readonly', true);

        $("#rowModButtonsDir").addClass("d-none");
        $("#rowButtonsDir").removeClass("d-none");

        $.ajax({
          type: "POST",
          url: url,
          data: $('#formDireccion').serialize(),
          success: after_direccion_actualizda,
          dataType: 'json'
        });
    });

    $('#mdiraCancelar').on('click', function (e) {
        e.preventDefault();
        $('input[name=tipo_via]').prop('readonly', true);
        $('input[name=nombre_via]').prop('readonly', true);
        $('input[name=nro_via]').prop('readonly', true);
        $('input[name=portalescalotros_via]').prop('readonly', true);
        $('input[name=piso_nroletra_via]').prop('readonly', true);
        $('input[name=cp_via]').prop('readonly', true);
        $('input[name=ciudad_via]').prop('readonly', true);
        $('input[name=provincia_via]').prop('readonly', true);
        $('input[name=pais_via]').prop('readonly', true);

        $("#rowModButtonsDir").addClass("d-none");
        $("#rowButtonsDir").removeClass("d-none");

    });


    function after_familia_actualizda(data) {
      if (data.status=='ok'){
          window.location.href = data.url;
      } else {
          alert("Error. Datos de familia NO actualizados");
      }
  }
  $('#btnModifFam').on('click', function (e) {

    e.preventDefault();

    let url = $('input[name=id]').val();

    $.ajax({
      type: "POST",
      url: url,
      data: $('#familyForm').serialize(),
      success: after_familia_actualizda,
      dataType: 'json'
    });
});

}

  window.addEventListener("load", botonesDireccion, false);


})(jQuery); // End of use strict