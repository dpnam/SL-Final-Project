$("#result-page").hide();
$("#upload-page").show();

function readURL(input) {
  if (input.files && input.files[0]) {

    $('#upload-page').fadeOut('fast', () => $('#result-page').fadeIn('fast'));

    const img = document.createElement("img");
    img.src = URL.createObjectURL(input.files[0]);
    img.onload = function() {
      URL.revokeObjectURL(this.src);
      $('#result-image-container').width(this.width).height(this.height);
    }
    $('#original-image-container').append(img);

    const spinnerContainer = document.createElement("div");
    spinnerContainer.className = "h-100 w-100 d-flex justify-content-center align-items-center";

    const spinner = document.createElement("div");
    spinner.className = "spinner-border";

    spinnerContainer.appendChild(spinner);
    $('#result-image-container').append(spinnerContainer);

    const formData = new FormData();
    formData.append("image", input.files[0]);

    fetch('/upload', {method: "POST", body: formData})
      .then(response => response.blob())
      .then(blob => {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(blob);
        img.onload = function() {
          URL.revokeObjectURL(this.src);
        }
        $('#result-image-container').empty().append(img);
      });
  } else {
    removeUpload();
  }
}

function removeUpload() {
  $('#file-upload-input').val("");
  $("#result-page").fadeOut('fast', () => {
    $("#upload-page").fadeIn('fast');
    $("#original-image-container").empty();
    $("#result-image-container").empty();
  });
}

$('.image-upload-wrap').bind('dragover', function () {
        $('.image-upload-wrap').addClass('image-dropping');
    });
    $('.image-upload-wrap').bind('dragleave', function () {
        $('.image-upload-wrap').removeClass('image-dropping');
});