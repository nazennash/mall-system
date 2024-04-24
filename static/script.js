document.addEventListener('DOMContentLoaded', function () {
	const items = document.querySelectorAll('.carousel-item');
	let currentIndex = 0;

	function cycleSlides() {
		items[currentIndex].classList.remove('active');

		currentIndex = (currentIndex + 1) % items.length;

		items[currentIndex].classList.add('active');
	}

	setInterval(cycleSlides, 3000);
});

function openChat() {
	var modal = document.getElementById('chatModal');
	modal.classList.remove('hidden');
}

function closeChat() {
	var modal = document.getElementById('chatModal');
	modal.classList.add('hidden');
}

function openModal() {
	var modal = document.getElementById('myModal');
	modal.classList.remove('hidden');
}

function closeModal() {
	var modal = document.getElementById('myModal');
	modal.classList.add('hidden');
}
