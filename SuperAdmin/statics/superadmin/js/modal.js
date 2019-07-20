

/* toggle modal open and close */
let body = document.getElementsByTagName('body')[0];
let uploader = document.getElementById('uploader');
let uploadClick = document.getElementById('upload-file');

if(uploadClick) {
    uploadClick.addEventListener('click', function(){
        // set body to overflow hidden
        body.setAttribute('class', 'modal-open');
        // show uploader modal
        uploader.style.display = 'block';
    }, false)
}

let backdrop = document.getElementsByClassName('media-modal-backdrop')[0];
let x = document.getElementsByClassName('media-modal-close')[0];

function closeModal() {
        // remove overflow hidden
        body.removeAttribute('class', 'modal-open');
        uploader.style.display = 'none';
    }

/* close modal when click  backdrop or close symbol */
if(backdrop) {
    backdrop.addEventListener('click',closeModal , false)
}

if(x) {
    x.addEventListener('click',closeModal , false)
}


/* menu button click */

let menus = document.getElementsByClassName('media-menu-item');
Array.from(menus).forEach(function(el) {

    el.addEventListener('click', function (event) {
        var isActive = el.classList.contains('active')
        if(!isActive) {
            el.classList.add('active');
            removeActive(menus, el)
        }
    }, false);
});

function removeActive(menus, el) {
    Array.from(menus).filter(element => element != el).forEach(function (element) {
        var isActive = el.classList.contains('active');
        if(isActive) {
            element.classList.remove('active');
        }

    });

}


var photos = document.getElementById('medial_library');
// ajax
 if(photos) {
     console.log('hello');
     photos.addEventListener('click',
     function GetImages() {
         let attachments =document.getElementsByClassName('attachments')[0];
         while(attachments.firstChild) {
             attachments.removeChild(attachments.firstChild)
         }
         var model = photos.getAttribute('model');
         var app = photos.getAttribute('app');
         var field = photos.getAttribute('field');
         var params = 'model_name='+model+'&app_name='+app+'&field_name='+field;
         var xhr = new XMLHttpRequest();
         xhr.onreadystatechange = function () {
              if(xhr.readyState == 4) {
                  console.log(xhr.responseText);
                  var images = JSON.parse(xhr.responseText);
                  renderImages(images, attachments);
                  toggleSelectPhoto(images);

             }
         }
        xhr.open('GET', '/superadmin/media-gallery.html'+'?'+params);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.send(null)
 }
     , false)
 }

 function renderImages(images, attachments) {
    for(var key in images) {
      let list = document.createElement('li');
      list.setAttribute('class', 'attachment');
      list.setAttribute('indexTag', key);
      let image = document.createElement('img');
      let div  = document.createElement('div');
      let button  = document.createElement('button');
      let span = document.createElement('span');
      span.setAttribute('class', 'media-modal-icon');
      button.setAttribute('type', 'button');
      button.setAttribute('class', 'checked');
      div.setAttribute('class', 'thumbnail');
      image.setAttribute('src', images[key]['url']);
      image.setAttribute('alt', images[key]['alt']);
      div.appendChild(image);
      list.appendChild(div);
      button.appendChild(span);
      list.appendChild(button);
      attachments.appendChild(list);
    }
 }


//click photo trigger even
function toggleSelectPhoto(images) {
    var attachments = document.getElementsByClassName('attachment');
    var lastChecked = [];

    if(attachments.length>0) {
        for(var i=0; i < attachments.length;i++){
            let attachment = attachments[i];
            attachment.addEventListener('click', function(event){
                var key = attachment.getAttribute('indexTag');
                var checkedIcon = attachment.getElementsByTagName('button')[0];
                if(attachment.classList.contains('selected')) {
                    attachment.classList.remove('selected')
                    checkedIcon.style.display = 'none';
                    const index = lastChecked.indexOf(attachment);
                    lastChecked.splice(index, 1);

                } else if(event.ctrlKey){
                    attachment.classList.add('selected');
                    checkedIcon.style.display = 'block';
                    selectedPhotoDetail(key, images);
                    lastChecked.push(attachment);
                } else {
                    attachment.classList.add('selected');
                    checkedIcon.style.display = 'block';
                    selectedPhotoDetail(key, images);
                    //uncheck last selected
                    if(lastChecked.length>0) {
                        for(let i=0; i < lastChecked.length; i++) {
                            let el = lastChecked.pop();
                            var lastCheckedIcon =el.getElementsByTagName('button')[0];
                            el.classList.remove('selected')
                            lastCheckedIcon.style.display = 'none';
                            console.log(lastChecked.length)

                        }

                    };
                    lastChecked.push(attachment);
                    console.log(lastChecked.length)
                }
            }, false)
        }

    }

}

function selectedPhotoDetail(key,images) {
    let image = images[key];
    let image_detail = document.getElementById('image-detail');
    let img_url = document.getElementById('thumbnail-image');
    let filename = document.getElementById('filename');
    let date = document.getElementById('date-uploaded');
    let dimension = document.getElementById('dimension');
    image_detail.indextag = key;
    img_url.src = image['url'];

    date.innerHTML = image['date'];
    filename.innerHTML = image['name'];
    dimension.innerHTML = image['dimension'];
}
         //
         // <div class="thumbnail thumbnail-image">
         //
         //                        </div>
         //                        <div class="details" id="image-detail">
         //                        <div id="filename"></div>
         //                        <div id="date-uploaded"></div>
         //                        <div id="file-size"></div>
         //                        <div id="dimension"></div>
         //                        <a href="#" class="edit-attachment" target="_blank">Edit Image</a>
         //                        <button class="button-link delete-attachment" type="button">Delete Permanently</button>