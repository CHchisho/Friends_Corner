console.log("Запустился файл");

function test_log() {
	console.log("Сработала функция test_log");
}
async function getid() {
	const id = document.getElementById('numberInput').value;
	// const name = document.getElementById('name').value;

	try {
		const response = await axios.post(`/pages/search_api/`+id, {
			id_2: id,
		});

		console.log(response.data);
		document.getElementById("demo1").innerHTML = `Полученный item_id: ${response.data.q}`;
	} catch (error) {
		console.error('Error:', error);
	}
}

// function getid() {
// 	var id = document.getElementById('numberInput').value;
//
// 	fetch('http://127.0.0.1:8000/pages/search_api/', {
// 		method: 'POST',
// 		body: JSON.stringify({ item_id: id })
// 	})
// 	.then(response => {
// 		if (!response.ok) {
// 			throw new Error(`Network response was not ok: ${response.statusText}`);
// 		}
// 		return response.json();
// 	})
// 	.then(data => {
// 		console.log('Полученные данные:');
// 		document.getElementById("demo1").innerHTML = `Полученный item_id: ${data.item_id}, Имя: ${data.name}`;
// 	})
// 	.catch(error => {
// 		console.log('Ошибка:', error);
// 	});
// }
