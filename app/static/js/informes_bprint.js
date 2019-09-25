function seguimientosElements(e) {

   $(document).on('click', '#btn_PDF_P', function (e) {
    $('#tbFiltroPersonas').attr("action", "/informes/pdf_personas");
    $('#tbFiltroPersonas').submit();
   });

}

window.addEventListener("load", seguimientosElements, false);