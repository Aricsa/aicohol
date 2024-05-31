fetch("static/json/data.json")
	.then((response) => response.json())
	.then((data) =>
	{
		console.log(data);
		const aicoholServicesContainer = document.getElementById('aicoholServices');
		aicoholServicesContainer.innerHTML = '';
		data.aicohol.forEach(service => {
			const serviceElement = document.createElement('div');
			if (service.img === "")
				service.img = "https://d1e2y5wc27crnp.cloudfront.net/media/smartorder_reservation/product_detail/e5dfc2c5-f4c5-46ab-91b7-2b13c5301482.webp"
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
				`<button class="bg-blue-500 text-white px-4 py-2 rounded ml-4" onclick="location.href='${detailViewUrl}'">상세보기</button>` +
			`</div>`;
			aicoholServicesContainer.appendChild(serviceElement);
		});
	})