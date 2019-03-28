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
 }

 $(document).on("click", ".asignar-dir", function (e) {

  var $row = $(this).closest("tr"); // Finds the closest row <tr>
  var dirid = $row.find("td:nth-child(1)").text().trim();

  $('input[name=idDir]').val(dirid);
  $("#cardBodyButtons").removeClass("d-none");
  $('#cardBodyDir').load('crear/loadDir/' + dirid);
  $('#myModal').modal('hide');
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

 window.addEventListener("load", botonesDireccion, false);