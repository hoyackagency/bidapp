$(document).ready(function() {
    var skills = $("#card-skills-value").data("skills").split(",");
    var skillsHtml = "";
    for (var i = 0; i < skills.length; i++) {
        var skill = skills[i].trim();
        skillsHtml += '<span class="badge badge-pill badge-primary">' + skill + '</span> ';
    }
    $("#card-skills-value").html(skillsHtml);
});