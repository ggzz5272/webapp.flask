const form = document.getElementById('addressForm');
const photoInput = document.getElementById('photo');
const photoPreview = document.getElementById('photoPreview');
const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('captureButton');

// 사진 미리보기
photoInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            photoPreview.src = e.target.result;
            photoPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        photoPreview.style.display = 'none';
    }
});

// 폼 제출 처리
form.addEventListener('submit', async function(event) {
    event.preventDefault(); // 기본 폼 제출 동작 막기

    const formData = new FormData(form);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        alert(result.message); // 서버 응답 메시지 표시
    } catch (error) {
        alert('데이터 전송 중 오류가 발생했습니다.');
    }
});

// 웹캠 스트림 시작
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error('웹캠 접근 실패:', err);
    });

// 촬영 버튼 클릭 이벤트
captureButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // 캡처된 이미지를 Base64로 변환
    const photoData = canvas.toDataURL('image/jpeg').split(',')[1];

    // 서버로 전송
    fetch('/capture_photo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ photo_data: photoData })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // 서버 응답 메시지 표시
    })
    .catch(err => {
        console.error('사진 업로드 실패:', err);
    });
});
