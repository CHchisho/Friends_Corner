let originalTasks = []; // Store original tasks to reset search
let originalTasks_content = [];

// Function for creating a new task
//document.getElementById('add_form').addEventListener('submit', function(event) {
//	event.preventDefault();
//	let title = document.getElementById('title').value;
//	let description = document.getElementById('description').value;
//	let status = document.getElementById('status').value;
//	let dueDate = document.getElementById('due-date').value;
//
//	// Create task object
//	let task = {
//	title: title,
//	description: description,
//	status: status,
//	dueDate: dueDate
//	};
//
//	// Call function to add task to table 
//	addTaskToTable_div(task);
//
//	// Reset form fields
//	document.getElementById('title').value = '';
//	document.getElementById('description').value = '';
//	document.getElementById('status').value = 'Todo';
//	document.getElementById('due-date').value = '';
//});


function addTaskToTable_div(task) {
	let tableBody = document.getElementById('content');
	let newRow = document.createElement('div');
	newRow.classList.add('full_task_block');
	newRow.innerHTML = `
	<div class="task_header">
		<h1>${task.title}</h1>
	</div>
	<h4 class="task_description">${task.description}</h4>
	<h4 class="task_status">${task.status}</h4>
	<h4 class="task_date">${task.dueDate}</h4>
	<div class="task_footer">				
		<button class="button button_edit" onclick="updateTask_div(this)"><i class="gg-pen"></i></button>
		<button class="button button_dele" onclick="deleteTask_div(this)">x</button>
	</div>
	`;
	// Changing the colour of the header
	let taskHeader = newRow.querySelector('.task_header');
	if (task.status==='Done') {taskHeader.classList.add('back_gre');}
	else if (task.status==='In progress') {taskHeader.classList.add('back_yel');}
	else if (task.status==='Todo') {taskHeader.classList.add('back_red');}
	tableBody.appendChild(newRow);

	originalTasks.push(newRow); // Save original task
//	console.log('block',originalTasks);
//	console.log('task',task)
	originalTasks_content.push(task);
	localStorage.setItem('data', JSON.stringify(originalTasks_content));
//	console.log('Сохраненный контент', JSON.parse(localStorage.getItem('data')));
}

// Deleting a task
function deleteTask_div(button) {
	let fullTaskBlock = button.closest('.full_task_block');

	let titleElement = fullTaskBlock.querySelector('.task_header h1').innerText;
	let descriptionElement = fullTaskBlock.querySelector('.task_description').innerText;
	let statusElement = fullTaskBlock.querySelector('.task_status').innerText;
	let dateElement = fullTaskBlock.querySelector('.task_date').innerText;
	let task = {
		title: titleElement,
		description: descriptionElement,
		status: statusElement,
		dueDate: dateElement,
	};
	
//	console.log('Delete', task)
//	console.log(originalTasks_content[0])
	
	const index = originalTasks_content.findIndex(item => 
		item.title === task.title && 
		item.description === task.description &&
		item.dueDate === task.dueDate
	);

//	console.log(originalTasks_content);
//	console.log(index);

	if (index !== -1) {
		originalTasks_content.splice(index, 1);
	}

	localStorage.setItem('data', JSON.stringify(originalTasks_content));
	fullTaskBlock.parentNode.removeChild(fullTaskBlock);
}


function updateTask_div(button) {
	let fullTaskBlock = button.closest('.full_task_block');

	let titleElement = fullTaskBlock.querySelector('.task_header h1');
	let descriptionElement = fullTaskBlock.querySelector('.task_description');
	let statusElement = fullTaskBlock.querySelector('.task_status');
	let dateElement = fullTaskBlock.querySelector('.task_date');


	// Create input fields with current values
	let titleInput = document.createElement('input');
	titleInput.type = 'text';
	titleInput.value = titleElement.innerText;

	let descriptionInput = document.createElement('textarea');
	descriptionInput.type = 'text';
	descriptionInput.value = descriptionElement.innerText;

	let statusInput = document.createElement('select');
	let statusOptions = ['Todo', 'In progress', 'Done'];
	statusOptions.forEach(option => {
		let statusOption = document.createElement('option');
		statusOption.value = option;
		statusOption.textContent = option.charAt(0).toUpperCase() + option.slice(1); 
		if (option === statusElement.innerText) {
			statusOption.selected = true;
		}
		statusInput.appendChild(statusOption);
	});

	let dueDateInput = document.createElement('input');
	dueDateInput.type = 'date';
	dueDateInput.value = dateElement.innerText;

	// Replace element contents with input fields
	const index = originalTasks_content.findIndex(item => 
		item.title === titleElement.innerHTML && 
		item.description === descriptionElement.innerHTML &&
		item.dueDate === dateElement.innerHTML &&
		item.status === statusElement.innerHTML
	);
	
	titleElement.innerHTML = '';
	titleElement.appendChild(titleInput);

	descriptionElement.innerHTML = '';
	descriptionElement.appendChild(descriptionInput);

	statusElement.innerHTML = '';
	statusElement.appendChild(statusInput);

	dateElement.innerHTML = '';
	dateElement.appendChild(dueDateInput);

	// Change button to 'Save' button
	button.textContent = 'Save';
	button.onclick = function () {
		// Update element contents with input field values
		titleElement.innerText = titleInput.value;
		descriptionElement.innerText = descriptionInput.value;
		statusElement.innerText = statusInput.value;
		dateElement.innerText = dueDateInput.value;

		// Remove class
		let task_head = fullTaskBlock.querySelector('.task_header');
		task_head.classList.remove('back_gre', 'back_yel', 'back_red');

		// Add class based on status
		if (statusInput.value === 'Done') {
			task_head.classList.add('back_gre');
		} else if (statusInput.value === 'In progress') {
			task_head.classList.add('back_yel');
		} else if (statusInput.value === 'Todo') {
			task_head.classList.add('back_red'); }
		

		console.log(index)
		console.log('1',originalTasks_content)
		if (index !== -1) {	
			originalTasks_content[index].title = titleInput.value;
			originalTasks_content[index].description = descriptionInput.value;
			originalTasks_content[index].dueDate = dueDateInput.value;
			originalTasks_content[index].status = statusInput.value;
			
//			originalTasks_content[index].title = '1111111111111111111111';
//			originalTasks_content[index].description = '1111111111111111111111';
//			originalTasks_content[index].dueDate = '1111111111111111111111';
//			originalTasks_content[index].status = '1111111111111111111111';
		}
		console.log('2', statusInput.value)
		localStorage.setItem('data', JSON.stringify(originalTasks_content));
		console.log('1',originalTasks_content)

		// Change button back to 'Update' button
		button.innerHTML = '<i class="gg-pen"></i>';
		button.onclick = function () { updateTask_div(this); };
	};
}


function searchTasks_div() {
	let searchText = document.getElementById('search_input').value.toLowerCase();
	let taskBlocks = document.querySelectorAll('.full_task_block');

	taskBlocks.forEach(taskBlock => {
		let title = taskBlock.querySelector('.task_header h1').innerText.toLowerCase();
		let description = taskBlock.querySelector('.task_description').innerText.toLowerCase();
		let status = taskBlock.querySelector('.task_status').innerText.toLowerCase();
		let dueDate = taskBlock.querySelector('.task_date').innerText.toLowerCase();

		if (title.includes(searchText) || description.includes(searchText) || status.includes(searchText) || dueDate.includes(searchText)) {
			taskBlock.style.display = ''; // Показать блок, если найдено совпадение
		} else {
			taskBlock.style.display = 'none'; // Скрыть блок, если совпадений не найдено
		}
	});
}




function resetSearch_div() {
	let taskBlocks = document.querySelectorAll('.full_task_block');

	taskBlocks.forEach(taskBlock => {
		taskBlock.style.display = ''; // Показать все блоки
	});

	document.getElementById('search_input').value = ''; // Очистить поле поиска
}







// localStorage.setItem('data', JSON.stringify(originalTasks));

// Функция для загрузки данных из Local Storage и отображения на странице
function loadData() {
    const storedData = localStorage.getItem('data');
    if (storedData) {
        const originalTasks_content = JSON.parse(storedData);
        // Отображаем данные на странице (в данном случае просто выводим в консоль)
        console.log('Loaded data: ', originalTasks_content);
		originalTasks_content.forEach(task => {
			addTaskToTable_div(task);
		});

    } else { console.log('No data in Local Storage'); }
}
window.onload = loadData;






//
//
// Create test tasks block
const titles = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5'];
const descriptions = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut diam sit amet nulla placerat fermentum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut diam sit amet nulla placerat fermentum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut diam sit amet nulla placerat fermentum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut diam sit amet nulla placerat fermentum.', 'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.', 'Quisque ut nisi ac tortor facilisis dapibus. Cras vel purus a odio hendrerit aliquam vel eu libero.', 'Fusce convallis velit nec nulla eleifend, eget mattis est posuere. Mauris at vehicula nisl.'];
const statuses = ['In progress', 'Done', 'Todo'];
const dueDates = ['2024-02-20', '2024-02-25', '2024-03-01', '2024-03-05', '2024-03-10'];


function generateRandomTask() {
	const randomTitle = titles[Math.floor(Math.random() * titles.length)];
	const randomDescription = descriptions[Math.floor(Math.random() * descriptions.length)];
	const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
	const randomDueDate = dueDates[Math.floor(Math.random() * dueDates.length)];

	return {
		title: randomTitle,
		description: randomDescription,
		status: randomStatus,
		dueDate: randomDueDate
	};
}

function create_test_tasks(button) {
	for (let i = 0; i < 8; i++) {
		const randomTask = generateRandomTask();
		addTaskToTable_div(randomTask);
	}		
	button.style.display = 'none';
}
//	  create_test_tasks();
// Create test tasks block
//
//


