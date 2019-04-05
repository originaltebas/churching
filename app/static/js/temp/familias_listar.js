function listarFamilias(e) {
    $(tblistarFamilias).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      }
    });
}

window.addEventListener("load", listarFamilias, false);