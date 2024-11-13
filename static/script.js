function selectButton(button, className) {
    // 해당 그룹의 모든 버튼에서 'selected' 클래스 제거
    const buttons = document.querySelectorAll(`.${className}`);
    buttons.forEach(btn => btn.classList.remove('selected'));

    // 클릭된 버튼에 'selected' 클래스 추가
    button.classList.add('selected');
}

function updateMargin(input) {
    // 현재 선택된 버튼에 여백을 적용
    const selectedButton = document.querySelector('.selected');
    if (selectedButton) {
        const marginValue = `${input.value}px`;
        selectedButton.style.marginBottom = marginValue;
    }
}

let uploadedFiles = []; // 이미 업로드된 파일들을 저장할 배열

function fileChangeHandler(files) {
    displayFiles(files);
}

function dropHandler(event) {
    event.preventDefault();
    document.getElementById('upload-area').classList.remove('drag-over');
    if (event.dataTransfer.files.length > 0) {
        displayFiles(event.dataTransfer.files);
    }
}

function displayFiles(files) {
    const preview = document.getElementById('upload-preview');
    const uploadIcon = document.querySelector('.upload-icon');
    const uploadText = document.querySelector('.upload-area p');

    // 파일이 업로드되면 아이콘과 텍스트 숨기기
    uploadIcon.style.display = 'none';
    uploadText.style.display = 'none';

    // 'preview'를 보이도록 설정 (파일 추가 시에만)
    preview.style.display = 'flex';

    Array.from(files).forEach(file => {
        // 동일한 파일이 이미 업로드된 경우를 확인
        if (!uploadedFiles.some(uploadedFile => uploadedFile.name === file.name && uploadedFile.size === file.size)) {
            uploadedFiles.push(file); // 새 파일 추가

            // 각 파일에 대한 HTML 요소 생성
            const fileItem = document.createElement('div');
            fileItem.classList.add('file-item');

            const fileIcon = document.createElement('span');
            fileIcon.classList.add('file-icon');
            fileIcon.textContent = '📄'; // 파일 아이콘으로 대체 가능

            const fileName = document.createElement('span');
            fileName.classList.add('file-name');
            fileName.textContent = file.name;

            const removeButton = document.createElement('button');
            removeButton.classList.add('remove-button');
            removeButton.textContent = '✖';
            removeButton.onclick = function() {
                fileItem.remove();  // 해당 파일 아이템만 제거
                uploadedFiles = uploadedFiles.filter(uploadedFile => uploadedFile.name !== file.name || uploadedFile.size !== file.size); // 배열에서 파일 제거

                // 파일이 모두 제거되면 아이콘과 텍스트 다시 표시
                if (uploadedFiles.length === 0) {
                    preview.style.display = 'none';
                    uploadIcon.style.display = 'block';
                    uploadText.style.display = 'block';
                }
            };

            fileItem.appendChild(fileIcon);
            fileItem.appendChild(removeButton);
            fileItem.appendChild(fileName);
            preview.appendChild(fileItem);
        }
    });
}

function dragOverHandler(event) {
    event.preventDefault();
    document.getElementById('upload-area').classList.add('drag-over');
}

// 드래그 상태에서 스타일 초기화
document.getElementById('upload-area').addEventListener('dragleave', () => {
    document.getElementById('upload-area').classList.remove('drag-over');
});


function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload/', {
        method: 'POST',
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            document.getElementById('result-image').src = url;
        })
        .catch(error => {
            alert('파일 업로드 중 오류가 발생했습니다.');
            console.error(error);
        });
}

function convertImage() {
    // 업로드된 파일이 있는지 확인
    if (uploadedFiles.length === 0) {
        alert("먼저 파일을 업로드하세요.");
        return;
    }

    // 첫 번째 파일을 변환 (다중 파일의 경우 루프를 추가 가능)
    const file = uploadedFiles[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload/', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("이미지 변환 중 오류가 발생했습니다.");
            }
            return response.blob();
        })
        .then(blob => {
            // 변환된 이미지를 표시하기 위해 Blob URL 생성
            const url = URL.createObjectURL(blob);
            document.getElementById('result-image').src = url;
        })
        .catch(error => {
            alert(error.message);
            console.error(error);
        });
}

function convertImages() {
    if (uploadedFiles.length === 0) {
        alert("먼저 파일을 업로드하세요.");
        return;
    }

    const formData = new FormData();
    uploadedFiles.forEach(file => {
        formData.append('file', file);
    });

    // 옵션 값 추가
    const mode = document.querySelector('.mode-button.selected').textContent.includes("다크") ? "dark" : "light";
    const ratio = document.querySelector('.ratio-button.selected').textContent;
    const margin = document.getElementById('margin-input').value;

    formData.append('mode', mode);
    formData.append('ratio', ratio);
    formData.append('margin', margin);

    fetch('/upload/', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("이미지 변환 중 오류가 발생했습니다.");
            }
            return response.blob();
        })
        .then(blob => {
            // Blob을 사용하여 자동으로 다운로드 시작
            const url = URL.createObjectURL(blob);
            const tempLink = document.createElement('a');
            tempLink.href = url;
            tempLink.download = 'converted_images.zip';
            document.body.appendChild(tempLink);
            tempLink.click();
            document.body.removeChild(tempLink);
            URL.revokeObjectURL(url); // URL 객체 해제
        })
        .catch(error => {
            alert(error.message);
            console.error(error);
        });
}