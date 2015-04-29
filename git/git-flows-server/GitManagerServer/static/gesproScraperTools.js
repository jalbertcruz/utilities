// Funciones para la extracción de información del GESPRO

function getGESPROProjects() {
    return _.map(_.filter($("#project_quick_jump_box option"), function (d) {
        return $(d).text().trim().startsWith('»');
    }), function (a) {
        return {text: $(a).text(), url: a["value"]};
    });
}
