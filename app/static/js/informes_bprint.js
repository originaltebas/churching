function seguimientosElements(e) {

  if ($('#tblistarSeguimientos').length != 0) {
    $(tblistarSeguimientos).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": ".",
      },
      "order": [],
    });
  }

  $(document).on('click', '#btn_PDF_P', function (e) {
    $('#tbFiltroPersonas').attr("action", "/informes/pdf_personas");
    $('#tbFiltroPersonas').submit();
  });

}

window.addEventListener("load", seguimientosElements, false);