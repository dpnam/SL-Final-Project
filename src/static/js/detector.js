const fileUploadInput = document.querySelector('#file-upload-input');
const imageUploadWrap = document.querySelector('#image-upload-wrap');

const resultImageContainer = document.querySelector('#result-image-container');
const originalImageContainer = document.querySelector('#original-image-container');

const modal = document.querySelector("#modal");
const modalImg = document.querySelector("#modal-img");
const modalCaption = document.querySelector("#modal-caption");
const modalClose = document.querySelector("#modal-close");

let controller = new AbortController();

imageUploadWrap.ondragenter = function() {
    this.classList.add('image-dropping');
};

imageUploadWrap.ondragleave = function() {
    this.classList.remove('image-dropping');
};

imageUploadWrap.ondrop = function() {
    this.classList.remove('image-dropping');
};

modalClose.onclick = function() {
  modal.style.display = "none";
}

function removeChildren(parent) {
    while (parent.firstChild) {
        parent.firstChild.remove();
    }
}

function createImage(obj, alt) {
    const img = document.createElement('img');
    img.src = URL.createObjectURL(obj);
    img.alt = alt;
    img.className = "image";
    // img.onload = function() {
    //     URL.revokeObjectURL(this.src);
    // }
    img.onclick = function() {
        modal.style.display = "block";
        modalImg.src = this.src;
        modalCaption.innerHTML = this.alt;
    }

    return img;
}

function upload(input) {
    if (input.files && input.files[0]) {
        clearAll();

        const img = createImage(input.files[0], "Uploaded Image");
        originalImageContainer.append(img);

        const loader = document.createElement('div');
        loader.className = 'loader';
        resultImageContainer.append(loader);

        const formData = new FormData();
        formData.append('image', input.files[0]);

        fetch(`${window.location.pathname}/upload`,
            { method: 'POST', body: formData, signal: controller.signal })
            .then(response => response.blob())
            .then(blob => {
                const img = createImage(blob, "Result Image");

                removeChildren(resultImageContainer);
                resultImageContainer.append(img);
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
    }
}

function clearAll() {
    controller.abort();
    controller = new AbortController();
    removeChildren(originalImageContainer);
    removeChildren(resultImageContainer);
}

