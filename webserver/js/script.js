$(document).ready(function() {
    const colors = ["black", "silver", "gray", "maroon", "red", "purple", "fuchsia", "green", "lime", "olive", "yellow", "navy", "blue", "teal", "aqua"]
    $("#title").on('click', function() {
        $(this).css("color", colors[Math.floor(Math.random() * colors.length)])
    });
})