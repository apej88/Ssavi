// 앨범 위에 정보 띄우는 스크립트
function displayAlbumInfo(albumElement) {
    var albumInfo = albumElement.querySelector('.album_info');
    if (albumInfo) {
        albumInfo.style.display = 'block';
    }
}

function hideAlbumInfo(albumElement) {
    var albumInfo = albumElement.querySelector('.album_info');
    if (albumInfo) {
        albumInfo.style.display = 'none';
    }
}

    var albums = document.querySelectorAll('.recom_item');

    albums.forEach(function(albumElement) {
        albumElement.addEventListener('mouseover', function() {
            displayAlbumInfo(albumElement);
        });

        albumElement.addEventListener('mouseout', function() {
            hideAlbumInfo(albumElement);
        });
    });


// 장르별 페이지 버튼 클릭하면 넘기는 자바스크립트.
// 슬라이드쇼 기능은 css에 들어있다. transition: transform 0.5s ease
const recomGroups = document.querySelectorAll(".recom-group");

recomGroups.forEach(group => {
    let pages = 0;
    const IMAGE_WIDTH = 1000;
    const backBtn = group.querySelector(".back");
    const nextBtn = group.querySelector(".next");
    const images = group.querySelectorAll(".recom_item");
    const all_page = images.length;

    console.log(all_page)

    function slideShow() {
        const positionValue = -pages * IMAGE_WIDTH;
        for (let i = 0; i < images.length; i++) {
            images[i].style.transform = `translateX(${positionValue}px)`;
        }
    }

    function next() {
        if (pages < all_page - 1) {
            pages += 1;
            slideShow();
            backBtn.removeAttribute('disabled');
            if (pages === all_page - 1) {
                nextBtn.setAttribute('disabled', 'true');
            }
        }
    }

    function back() {
        if (pages > 0) {
            pages -= 1;
            slideShow();
            nextBtn.removeAttribute('disabled');
            if (pages === 0) {
                backBtn.setAttribute('disabled', 'true');
            }
        }
    }

    function init() {
        backBtn.setAttribute('disabled', 'true');
        backBtn.addEventListener("click", back);
        nextBtn.addEventListener("click", next);
    }

    init();
});
