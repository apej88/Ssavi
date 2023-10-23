// 앨범 위에 정보 띄우는 스크립트
function displayAlbumInfo(albumElement) {
    var albumInfo = albumElement.querySelector('.album_info');
    albumInfo.style.display = 'block';
    }

    function hideAlbumInfo(albumElement) {
    var albumInfo = albumElement.querySelector('.album_info');
    albumInfo.style.display = 'none';
    }

    function likeAlbum(albumElement) {
    // 좋아요 처리 로직 추가
    alert('좋아요가 클릭되었습니다.');
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


// 슬라이드쇼 관련 스크립트
// 첫 번째 요소
let pages = 0;
let positionValue = 0;
const IMAGE_WIDTH = 1000;
const backBtn = document.querySelectorAll(".back")
const nextBtn = document.querySelectorAll(".next")
const images = document.querySelectorAll(".recom_item")
all_page = images.length
console.log(all_page)

// 다음으로 가는 기능
function next() {
    if (pages < all_page) {
        backBtn.forEach(btn => btn.removeAttribute('disabled'));
        for (let i = 0; i < images.length; i++) {
            images[i].style.transform = `translateX(${positionValue - 1000}px)`;
        }
        positionValue -= IMAGE_WIDTH;
        pages += 1;
        if (pages === all_page) {
            nextBtn.forEach(btn => btn.setAttribute('disabled', 'true'));
        }
    }
};

// 이전으로 가는 기능
function back() {
    if (pages > 0) {
        nextBtn.forEach(btn => btn.removeAttribute('disabled'));
        for (let i = 0; i < images.length; i++) {
            images[i].style.transform = `translateX(${positionValue + 1000}px)`;
        }
        positionValue += IMAGE_WIDTH;
        pages -= 1;
        if (pages === 0) {
            backBtn.forEach(btn => btn.setAttribute('disabled', 'true'));
        }
    }
};

function init() {
    backBtn.forEach(btn => btn.setAttribute('disabled', 'true'));
    backBtn.forEach(btn => btn.addEventListener("click", back));
    nextBtn.forEach(btn => btn.addEventListener("click", next));
};

init();