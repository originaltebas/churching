function extrasElements(e) {

  // EXTRAS -> Estados Civiles
  if ($('#tblistarEstadosCiviles').length != 0) {
    $(tblistarEstadosCiviles).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      }
    });
  }

  // EXTRAS -> Tipos de Miembros
  if ($('#tblistarTiposMiembros').length != 0) {
    $(tblistarTiposMiembros).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      }
    });
  }

  // EXTRAS -> Rles Familiares
  if ($('#tblistarRolesFamiliares').length != 0) {
    $(tblistarRolesFamiliares).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      }
    });
  }

    // EXTRAS -> Tipos de Familias
    if ($('#tblistarTiposFamilias').length != 0) {
      $(tblistarTiposFamilias).dataTable({
        "language": {
          "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
          "decimal": ",",
          "thousands": "."
        }
      });
    }


}
window.addEventListener("load", extrasElements, false);