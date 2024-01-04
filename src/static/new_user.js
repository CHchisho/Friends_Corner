

var hobbies_ = [];
function submitForm() {
//	console.log(document.getElementById('about_you').value);
	const checks = document.querySelectorAll('input[name="hobby"]');
	hobbies_ = [];
	checks.forEach(el => {if (el.checked) {hobbies_.push(el.value);}});
	
	
	try { 
		const fileInput1 = document.getElementById('fileInput1');
		const fileInput2 = document.getElementById('fileInput2');

		const file1 = fileInput1.files[0];
		const file2 = fileInput2.files[0];

		const formData = new FormData();
		formData.append('file1', file1);
		formData.append('file2', file2);

		axios.post('/auth/photos', formData)
		.then(response => {
			finish_reg();
		})
		.catch(error => {
			console.error('Error:', error);
		});
		
		}
	catch (error) {console.error(error);}
	
}


function finish_reg () {
	try {
		axios.post('/auth/register', 
		{
			email: document.getElementById('email').value,
			password: document.getElementById('password').value,
			is_active: true,
			is_superuser: false,
			is_verified: false,
			username: document.getElementById('username').value,
			phone_number: document.getElementById('phonenumber').value,
			gender: document.querySelector('input[name="gender_you"]:checked').value,
			regions: document.getElementById('regions').value,
			your_age: document.getElementById('your_age').value,
			hobbies: hobbies_.join('&'),
			about_you: document.getElementById('about_you').value,
			friend_gender: document.querySelector('input[name="gender_friend"]:checked').value,
			friend_age_from: document.getElementById('friend_age_from').value,
			friend_age_to: document.getElementById('friend_age_to').value,
		}
		)
		.then(res => {
			alert("Success!");
			var relativePath = '/pages/login';
			var baseURL = window.location.origin;
			var fullURL = baseURL + relativePath;
			window.open(fullURL, '_blank');	
		})
		.catch(err => {
		console.log(err);alert('err1');alert(err);
		});
	}
	catch (error) {console.error(error);alert('err2');alert(error);}
	
}

function checkCheckboxes() {
      var checkboxes = document.getElementsByName("hobby");
      var checkedCount = 0;
      for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {checkedCount++;}}
      if (checkedCount < 3) {
        document.getElementById("p_error").textContent = "Please select at least 3 hobbies.";
        return 0;
      } else {
        document.getElementById("p_error").textContent = "";
		return 1;
      }
    }

    // Вызываем функцию при изменении состояния флажков
document.addEventListener("change", checkCheckboxes);