let body = document.getElementsByTagName('body')[0];
let uploader = document.getElementById('uploader');

let uploadClick = document.getElementById('upload-file');

if(uploadClick) {
    uploadClick.addEventListener('click', function(){
        body.setAttribute('class', 'modal-open');
        uploader.style.display = 'block';
    }, false)
}



let backdrop = document.getElementsByClassName('media-modal-backdrop')[0];
let x = document.getElementsByClassName('media-modal-close')[0];

function closeModal() {
        body.removeAttribute('class', 'modal-open');
        uploader.style.display = 'none';
    }
if(backdrop) {

    backdrop.addEventListener('click',closeModal , false)
}

if(x) {
    x.addEventListener('click',closeModal , false)
}