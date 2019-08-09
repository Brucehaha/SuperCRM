"use strict";
(function() {

    /* toggle modal open and close */
    let body = document.getElementsByTagName('body')[0];
    let uploader = document.getElementById('uploader');
    let uploadClick = document.getElementById('upload-files');
    // display modal
    if (uploadClick) {
        uploadClick.addEventListener('click', function () {
            // set body to overflow hidden
            body.setAttribute('class', 'modal-open');
            // show uploader modal
            uploader.style.display = 'block';
        }, false)
    }
    let backdrop = document.getElementsByClassName('media-modal-backdrop')[0];
    let x = document.getElementsByClassName('media-modal-close')[0];
    //close modal
    function closeModal() {
        // remove overflow hidden
        body.removeAttribute('class', 'modal-open');
        uploader.style.display = 'none';
    }

    /* close modal when click  backdrop or close symbol */
    if (backdrop) {
        backdrop.addEventListener('click', closeModal, false)
    }

    if (x) {
        x.addEventListener('click', closeModal, false)
    }


    /* menu button click */
    $(".media-menu-item").click(function() {
        console.log($(this));
        let isActive = $(this).hasClass('active')
        if (!isActive) {
            $(this).addClass('active');
            removeActive(this)
        }
    }
    );


    function removeActive(el) {
        $(".media-menu-item").each(function() {
            let isActive = $(this).hasClass('active');
            if (isActive && this !== el) {
                 $(this).removeClass('active');
            }
        });

    }

    var images;
    var model;
    var app;
    var field;
    var modal = document.getElementById('upload-files');

// xhr loading photos
    if(modal){
        modal.addEventListener('click',
        function GetImages(e) {
            console.log(e.target);
            var photos = document.getElementById('medial_library');
            console.log(photos)
            let attachments = document.getElementsByClassName('attachments')[0];
            while (attachments.firstChild) {
                attachments.removeChild(attachments.firstChild)
            }
            model = photos.getAttribute('model');
            app = photos.getAttribute('app');
            field = photos.getAttribute('field');
            var params = 'model_name=' + model + '&app_name=' + app + '&field_name=' + field;
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4) {
                    images = JSON.parse(xhr.responseText);
                    renderImages(images, attachments);
                    toggleSelectPhoto(images);

                }
            }
            xhr.open('GET', '/superadmin/media-gallery.html' + '?' + params);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

            xhr.send(null)
        }
        , false)


    }

    function renderImages(images, attachments) {
        for (var key in images) {
            let list = document.createElement('li');
            list.setAttribute('class', 'attachment');
            list.setAttribute('indexTag', key);
            let image = document.createElement('img');
            let div = document.createElement('div');
            let button = document.createElement('button');
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

    var lastChecked = [];

//click photo trigger even
    function toggleSelectPhoto(images) {
        var attachments = document.getElementsByClassName('attachment');
        if (attachments.length > 0) {
            for (var i = 0; i < attachments.length; i++) {
                let attachment = attachments[i];
                var attachment_details = document.getElementById('attachment_details');
                attachment.addEventListener('click', function (event) {
                    var key = attachment.getAttribute('indexTag');
                    var checkedIcon = attachment.getElementsByTagName('button')[0];
                    if (attachment.classList.contains('selected')) {
                        attachment.classList.remove('selected');
                        checkedIcon.style.display = 'none';
                        removeExistedSinglePhotoFromArray(attachment);
                    } else if (event.ctrlKey) {
                        attachment.classList.add('selected');
                        checkedIcon.style.display = 'block';
                        selectedPhotoDetail(key, images);
                        attachment_details.style.display= 'block';
                        lastChecked.push(attachment);
                    } else if (event.shiftKey && lastChecked.length > 0) {
                        rangeSelectPhoto(attachment, checkedIcon, key, images);
                        attachment_details.style.display= 'block';

                    } else {
                        selectSinglePhoto(attachment, checkedIcon, key, images);
                        attachment_details.style.display= 'block';

                    }
                }, false)
            }

        }

    }

    Array.prototype.multiIndexOf = function (el) {
        var idxs = [];
        for (var i = 0; i < this.length; i++) {
            if (this[i] === el) {
                idxs.push(i);
            }
        }
        return idxs;
    };


// select single photo can uncheck all others
    function selectSinglePhoto(attachment, checkedIcon, key, images) {
        attachment.classList.add('selected');
        checkedIcon.style.display = 'block';
        selectedPhotoDetail(key, images);
        if (lastChecked.length > 0) {
            const total = lastChecked.length;
            for (let i = 0; i < total; i++) {
                let el = lastChecked[i];
                if (el !== attachment) {
                    let lastCheckedIcon = el.getElementsByTagName('button')[0];
                    el.classList.remove('selected');
                    lastCheckedIcon.style.display = 'none';
                }

            }
        }
        ;
        lastChecked = [];
        lastChecked.push(attachment);
        console.log(lastChecked)

    }

// remove the existing key
    function removeExistedSinglePhotoFromArray(attachment) {
        const index = lastChecked.indexOf(attachment);
        // console.log(lastChecked)
        // console.log(attachment);

        // remove the attachment already selected
        lastChecked.splice(index, 1);


    }

    function selectedPhotoDetail(key, images) {
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
    // get image ids' list
    function ImageIdList(elList) {
        let indexList = [];
        for (let index = 0; index < lastChecked.length; index++) {
            let tagId = lastChecked[index].getAttribute('indextag');
            indexList.push(parseInt(tagId));
        }
        return indexList
    }

    function rangeSelectPhoto(attachment, checkedIcon, key, images) {
        var indexList = ImageIdList(lastChecked);
        let maxNum = Math.max(...indexList);
        let minNum = Math.min(...indexList);
        let currentNum = attachment.getAttribute('indextag');
        if (parseInt(currentNum) > maxNum) {
            rangeSelect(currentNum, minNum, lastChecked)
        } else if (parseInt(currentNum) < minNum) {
            rangeSelect(maxNum, currentNum, lastChecked);
        } else {
            selectSinglePhoto(attachment, checkedIcon, key, images);

        }

    }

// select range by pressing shift
    function rangeSelect(max, min) {
        let el = document.getElementsByClassName('attachments')[0];
        for (let i = min; i <= max; i++) {
            let att = el.querySelectorAll('[indextag="' + i + '"]')[0];
            if (!lastChecked.includes(att)) {
                let checkedIcon = att.getElementsByTagName('button')[0];
                att.classList.add('selected');
                checkedIcon.style.display = 'block';
                lastChecked.push(att);
            }
        }
    }

    /* add photo to the input box prepare for submiting to the database */
    var addToGallery = document.getElementById('add-to-gallary');
    if(addToGallery){
        addToGallery.addEventListener('click', function (event) {
            closeModal()
            let idList = ImageIdList(lastChecked);
            console.log(idList)

            for(let i = 0; i < idList.length;i++) {
                getSelectedImages(idList[i])
            }
        }, false);
    }


    var photoHTML1 = `
        
            <div class="initLoading" style="display:none;">
                <img src="/static/superadmin/imgs/img_loading.gif" alt="" class="loading-img">
            </div>
            <div class="show-img">
                    <a class="remove" href="javascript:void(0)" tag="image-{{ id }}">
                        <img src="/static/superadmin/imgs/removeUpload.png" alt="">
                    </a>
                    <div class="reupload-hover">
                        <a href="javascript:void(0)" class="release-dialog-update" >
                            <img class='pic' src="`;

     var photoHTML2 =  `">
                        </a>
                    </div>
            </div>
         `;

    function getSelectedImages(key) {
        var selectedOptions = getExistedPhotos();
        if(!selectedOptions.includes(key.toString())){
            var id = 'image-'+key
            // append picture to the main page
            var newPic = document.createElement('div');
            newPic.classList.add('check');
            newPic.innerHTML = photoHTML1 + images[key]['url'] +photoHTML2;
            newPic.getElementsByClassName('remove')[0].setAttribute('tag', id);
            var modal = document.getElementsByClassName('pic-postion')[0]
            modal.insertBefore(newPic, document.getElementById('upload-files'));
            // append select option
            var option = document.createElement('option');
            option.setAttribute('id', id);
            option.setAttribute('selected', true);
            option.setAttribute('value', key);
            var select = document.getElementById('id_'+ field +'_from');

            select.appendChild(option);
        }
    }
    function getExistedPhotos() {
        var select = document.getElementById('id_'+ field +'_from');

        var options = select.getElementsByTagName('option');
        var selectImages = []
        for(let i=0; i < options.length; i++) {
            selectImages.push(options[i].value);
        }
        return selectImages;
    }
})()
