document.addEventListener('DOMContentLoaded', (event) => {
    const urlParams = new URLSearchParams(window.location.search);
    const serviceId = urlParams.get('id');
    fetch("../static/json/data.json")
    .then((response) => response.json())
    .then((data) =>
    {
        const aicoholServicesContainer = document.getElementById('aicoholServicesDetail');
        aicoholServicesContainer.innerHTML = '';
        const service = data.aicohol.find(({id}) => id === Number(serviceId));
        const serviceElement = document.createElement('div');
        serviceElement.classList.add('flex', 'items-start'); // 이미지와 정보를 가로로 배치하기 위해 flex 클래스 추가
        serviceElement.innerHTML =
        `<div class="w-1/2">` +
            `<div class="bg-gray-300 h-96 w-full flex items-center justify-center rounded">` + // 이미지 영역 높이를 96px로 늘림
            `<img src="${service.img}" alt="${service.name}" class="w-full h-full object-cover">` +
            `</div>` +
        `</div>` +
        `<div class="w-1/2 pl-6 py-6">` + // 정보 영역 패딩을 6px씩 늘림
            `<p class="text-lg"><strong>종류: ${service.type}</strong></p>` +
            `<p class="text-lg"><strong>이름: ${service.name}</strong></p>` +
            `<p class="text-lg"><strong>도수: ${service.ABV}</strong></p>` +
            `<p class="text-lg"><strong>국가: ${service.nation}</strong></p>` +
            `<p class="text-lg"><strong>설명: ${service.desc}</strong></p>` +
            `<p class="text-lg"><strong>맛, 향: ${service.tasting}</strong></p>` +
        `</div>`
        console.log(serviceElement);
        aicoholServicesContainer.appendChild(serviceElement);
    })
});
