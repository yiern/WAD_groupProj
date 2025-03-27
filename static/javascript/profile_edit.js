document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('profile_picture');
  const preview = document.getElementById('preview');

  input.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        preview.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
});
