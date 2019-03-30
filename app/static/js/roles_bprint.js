function rolesElements(e) {

  // Roles -> Estados Civiles
  if ($('#tbListarRoles').length != 0) {
    $(tbListarRoles).dataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
        "decimal": ",",
        "thousands": "."
      }
    });
  }
}
window.addEventListener("load", rolesElements, false);
