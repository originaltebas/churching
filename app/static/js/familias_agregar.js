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


 window.addEventListener("load", botonesDireccion, false);