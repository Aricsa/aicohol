fetch("static/json/data.json")
	.then((response) => response.json())
	.then((data) =>
	{
		const aicoholServicesContainer = document.getElementById('aicoholServices');
		aicoholServicesContainer.innerHTML = '';
		data.aicohol.forEach(service => {
			const serviceElement = document.createElement('div');
			serviceElement.innerHTML +=
			`<div class="bg-white shadow rounded p-4 mb-4 flex items-center">` +
				`<div class="flex-1">` +
					`<p><strong>종류: ${service.type}</strong></p>` +
					`<p><strong>이름: ${service.name}</strong></p>` +
					`<p><strong>도수: ${service.ABV}%</strong></p>` +
				`</div>` +
				`<div class="w-24 h-24 bg-gray-300 flex-shrink-0">` +
					`<img src="${service.img}" alt="${service.name}" class="w-full h-full object-cover">` +
				`</div>` +
					`<button class="bg-blue-500 text-white px-4 py-2 rounded ml-4" onclick="location.href='${detailViewUrl}?id=${service.id}'">상세보기</button>` +
			`</div>`;
			aicoholServicesContainer.appendChild(serviceElement);
		});
	})

function getFilteredServicesNameInputValue()
{
	fetch("static/json/data.json")
	.then((response) => response.json())
	.then((data) =>
	{
		const inputElement = document.getElementById('filteredServicesNameSearch').value;
		const service = filteredServiceByName(data.aicohol, inputElement)[0];
		const aicoholServicesContainer = document.getElementById('filterdService');
		aicoholServicesContainer.innerHTML = '';

		const titleElement = document.createElement('h2');
		titleElement.textContent = '검색 결과';
		titleElement.classList.add('text-xl', 'font-bold', 'mb-4');
		aicoholServicesContainer.appendChild(titleElement);

		const serviceElement = document.createElement('div');
		if (service) {
			serviceElement.innerHTML +=
			`<div class="bg-white shadow rounded p-4 mb-4 flex items-center">` +
				`<div class="flex-1">` +
					`<p><strong>종류: ${service.type}</strong></p>` +
					`<p><strong>이름: ${service.name}</strong></p>` +
					`<p><strong>도수: ${service.ABV}%</strong></p>` +
				`</div>` +
				`<div class="w-24 h-24 bg-gray-300 flex-shrink-0">` +
					`<img src="${service.img}" alt="${service.name}" class="w-full h-full object-cover">` +
				`</div>` +
					`<button class="bg-blue-500 text-white px-4 py-2 rounded ml-4" onclick="location.href='${detailViewUrl}?id=${service.id}'">상세보기</button>` +
			`</div>`;
			aicoholServicesContainer.appendChild(serviceElement);
		}
		else {
			const noResultElement = document.createElement('div');
			noResultElement.innerHTML = `<div class="text-center p-4">검색 결과가 없습니다.</div>`;
			aicoholServicesContainer.appendChild(noResultElement);
		}
		
		const spacerElement = document.createElement('div');
		spacerElement.style.height = '1rem';
		aicoholServicesContainer.appendChild(spacerElement);
	});
}

const filteredServiceByName = (services, name) => 
	services.filter(service => service.name.toLowerCase().includes(name.toLowerCase()));


