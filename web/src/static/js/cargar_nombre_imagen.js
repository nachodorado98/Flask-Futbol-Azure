const inputFile = document.getElementById('imagen');
const botonLabel = document.getElementById('botonLabel');
const nombreArchivo = document.getElementById('nombre-archivo-imagen');

inputFile.addEventListener('change', function () {
  if (inputFile.files.length > 0) {

    const fileName = inputFile.files[0].name;

    botonLabel.textContent = fileName;

    nombreArchivo.textContent = ''
  } else {

    botonLabel.textContent = 'Seleccionar Archivo';
    nombreArchivo.textContent = 'Ningún archivo seleccionado';
  }
});