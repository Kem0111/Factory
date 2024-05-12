document.getElementById('image_1').addEventListener('change', function(event) {
    var output = document.getElementById('image_preview');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src)
    }
    output.style.display = 'block';
});