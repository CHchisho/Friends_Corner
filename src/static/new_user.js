

function submitForm() {
	
	const checks = document.querySelectorAll('input[name="hobby"]');
	let hobbies = [];
	checks.forEach(el => {if (el.checked) {hobbies.push(el.value);}});
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
			hobbies: hobbies.join('&'),
			friend_gender: document.querySelector('input[name="gender_friend"]:checked').value,
			friend_age_from: document.getElementById('friend_age_from').value,
			friend_age_to: document.getElementById('friend_age_to').value,
		}
		)
//			.then(res => {
//				document.getElementById('demo1').textContent = res.data.qdata;
//			})
		.catch(err => {
		console.log(err);
		});
	}
	catch (error) {console.error(error);}
	
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
			console.log('Success:', response.data);
		})
		.catch(error => {
			console.error('Error:', error);
		});
		alert("Success!");
		}
	catch (error) {console.error(error);}}


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