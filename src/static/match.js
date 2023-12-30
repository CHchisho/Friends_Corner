

	var client_id=document.getElementById('userdata_id').innerHTML;

	var friend_id = 1;
	
	var request = 0;
	let matchArray = [];
//	var user_id_recipient = 1;
	
//	document.getElementById('id').textContent = client_id;
	
	function get_new_match(){
//		clearContainer()
//		user_id_recipient = id;
//		console.log('Selected ID: ', user_id_recipient);
		axios.get('/chat/match/'+client_id, {
		  headers: { 'Accept': 'application/json' }
		})
		.then(messages => {
			console.log(messages.data);
			matchArray = messages.data;
			
			if (matchArray.length > 0) {update_info(0);}
			else {no_anymore();}
			
		})
		.catch(error => {console.error(error);});
	}
	get_new_match();


//function submitForm() {
//	try {
//		axios.post('/chat/match'+client_id,
//		{
//			email: document.getElementById('email').value,
//			password: document.getElementById('password').value,
//		}, {headers: { 'Accept': 'application/json' }})
////		.then(res => {
////			console.log(res.data);
////		})
//		.catch(err => {console.log(err);});
//	}
//	catch (error) {console.error(error);}}
	
function send_answer_match(answer_) {
	try {
		axios.post('/chat/match/',
		{
			id_sender: client_id,
			id_recipient: friend_id,
			answer: answer_,
		}, {headers: { 'Accept': 'application/json' }})
		.then(res => {
//			console.log(res.data);
			
			console.log('get answer from post');
			console.log(request);
			
			if (request<4){
		//		1
				if (request+2 > matchArray.length  && matchArray.length < 5){no_anymore();return;}
				
				request++;
				update_info(request);
			}
			else {
				get_new_match();
				console.log('get_new_match start')
				request=0;
			}
			
			
		})
		.catch(err => {console.log(err);});
	}
	catch (error) {console.error(error);}	
//	alert('Button clicked: ' + answer_);
//	alert('New user:');
}

	
// Обновляет информацию о человеке в правом контейнере
function update_info(id_){
	try {
	friend_id = matchArray[id_].id;
	document.getElementById('name').textContent = matchArray[id_].username+', '+matchArray[id_].your_age + ', '+matchArray[id_].gender;
//	document.getElementById('age').textContent = matchArray[id_].your_age;
//	document.getElementById('id').textContent = matchArray[id_].id;
//	document.getElementById('id').textContent = '';
//	document.getElementById('region').textContent = "I'm from: " + matchArray[id_].regions.charAt(0).toUpperCase() + matchArray[id_].regions.slice(1);
	document.getElementById('region').textContent = "I'm from: " + matchArray[id_].regions;
	document.getElementById('hobbies').textContent = "My hobbies: " + matchArray[id_].hobbies.split('&').join(', ');
	document.getElementById('info').textContent = "More about me: " + matchArray[id_].about_you;

	let imagePath = matchArray[id_].id + '_1.jpg';
	document.getElementById('container').style.backgroundImage = 'url("{{ url_for("static", path="photos/") }}' + imagePath + '")';
	}
	catch (error) {console.error(error);}
}
	

// Срабатывает, когда нет больше подходящих кандидатов
function no_anymore(){
	document.getElementById('name').textContent = 'Sorry, there are no suitable candidates yet.';
//	document.getElementById('age').textContent = '';
//	document.getElementById('id').textContent = '';
	document.getElementById('info').textContent = '';
	document.getElementById('hobbies').textContent = '';
	
	document.getElementById('region').textContent = '';

	let imagePath = 'nobody.jpg';
	document.getElementById('container').style.backgroundImage = 'url("{{ url_for("static", path="photos/") }}' + imagePath + '")';
}
	
	
// Переключает фотографии человека
let image_number=1;
function select_image() {
	document.getElementById('container').style.backgroundImage = 'url("{{ url_for("static", path="photos/") }}' + matchArray[request].id + '_'+image_number+'.jpg' + '")';
	image_number = (image_number === 1) ? 2 : 1;
}
	
//function createElements(sender, recipient, msg, date) {
//	var container = document.getElementById('container');
//	var messageDiv = document.createElement('div');
//	var dateBlock = document.createElement('div');
//	dateBlock.textContent = date;
//
//	var p = document.createElement('p');
//	if (sender==client_id) {
//		p.innerHTML = msg;
//		p.classList.add('odd');
//		dateBlock.classList.add('dateBlock_odd');
//	} else {
//		p.textContent = msg;
//		p.classList.add('even');
//		dateBlock.classList.add('dateBlock_even');
//	}
//	messageDiv.appendChild(p);
//	messageDiv.appendChild(dateBlock);
//	container.appendChild(messageDiv);
//}
	
//	function clearContainer() {
//		var container = document.getElementById('container');
//		container.innerHTML = ''; // Устанавливаем пустую строку в качестве содержимого
//	}
	
//    function appendMessage(msg) {
//        let messages = document.getElementById('messages')
//        let message = document.createElement('li')
//        let content = document.createTextNode(msg)
//        message.appendChild(content)
//        messages.appendChild(message)
//    }