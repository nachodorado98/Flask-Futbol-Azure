const inputFile = document.getElementById('imagen');
const preview = document.getElementById('preview');
const mensaje = document.getElementById('mensaje');
const botonLabel = document.getElementById('botonLabel');

inputFile.addEventListener('change', function () {
  const file = inputFile.files[0];

  if (file) {
    const fileType = file.type.toLowerCase();

    if (fileType === "image/jpeg" || fileType === "image/jpg" || fileType === "image/png") {
      const reader = new FileReader();

      reader.onload = function (e) {
        preview.src = e.target.result;
        preview.style.display = "block";
        mensaje.textContent = "";
        botonLabel.textContent = file.name; 
      };

      reader.readAsDataURL(file);
    } else {
      preview.style.display = "none";
      mensaje.textContent = "El archivo no es válido";
      botonLabel.textContent = "Seleccionar Imagen";
    }
  } else {
    preview.style.display = "none";
    mensaje.textContent = "No se ha seleccionado ninguna imagen";
    botonLabel.textContent = "Seleccionar Imagen";
  }
});
