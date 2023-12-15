

//function submitForm() {
//	console.log(document.getElementById('email').value);
//	console.log(document.getElementById('password').value);
//	try {
//		axios.post('/auth/login', 
//		{
//			username: document.getElementById('email').value,
//			password: document.getElementById('password').value,
//		}
//		)
////			.then(res => {
////				document.getElementById('demo1').textContent = res.data.qdata;
////			})
//		.catch(err => {
//		console.log(err);
//		});
//	}
//	catch (error) {console.error(error);}
//	}

function submitForm() {
try {
	const headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/x-www-form-urlencoded'
};

const data = new URLSearchParams();
data.append('grant_type', '');
data.append('username', document.getElementById('email').value);
data.append('password', document.getElementById('password').value);
data.append('scope', '');
data.append('client_id', '');
data.append('client_secret', '');

axios.post('/auth/login', data, { headers })
//  .then(response => {
//    console.log(response.data);
//  })
  .catch(error => {
    console.error(error);
  });
alert('Login!');

	
var relativePath = 'pages/search';

// Получаем базовый URL текущей страницы
var baseURL = window.location.origin;

// Составляем полный URL с относительным путем
var fullURL = baseURL + '/' + relativePath;

// Открываем новую вкладку
window.open(fullURL, '_blank');
}
catch (error) {console.error(error);}
}





function submitFormout() {
try {
const headers = {
  'Accept': 'application/json'
};

axios.post('/auth/logout', null, { headers })
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error(error);
  });

alert('Logout!');
}
catch (error) {console.error(error);}
}