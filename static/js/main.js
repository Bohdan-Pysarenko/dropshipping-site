const bar = document.getElementById('bar')
const close = document.getElementById('close')
const nav = document.getElementById('categories')

if (bar) {
	bar.addEventListener('click', () => {
		nav.classList.add('active')
	})
}

if (close) {
	close.addEventListener('click', () => {
		nav.classList.remove('active')
	})
}


//   Image carousel
const carouselContainer = document.querySelector('.little-sticky-container');
const carousel = document.querySelector('.small-img-group');
const images = document.querySelectorAll('.small-img-group img');

let currentIndex = 0;

// Функція для переміщення каруселі на попередню картинку
function prevImage() {
  currentIndex = (currentIndex - 1 + images.length) % images.length;
  updateCarousel();
}

// Функція для переміщення каруселі на наступну картинку
function nextImage() {
  currentIndex = (currentIndex + 1) % images.length;
  updateCarousel();
}

// Функція для оновлення відображення каруселі
function updateCarousel() {
  const translateValue = -currentIndex * 100; // 100% на одну картинку
  carousel.style.transform = `translateX(${translateValue}%)`;
}

// Додайте події для слайдів по дотику (swipe)
let touchStartX = null;
let touchEndX = null;

carouselContainer.addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
});

carouselContainer.addEventListener('touchend', (e) => {
  touchEndX = e.changedTouches[0].clientX;
  
  // Визначаємо, чи був зроблений свайп вліво чи вправо
  const swipeDistance = touchEndX - touchStartX;
  if (swipeDistance > 50) {
    prevImage(); // Свайп вправо - попередня картинка
  } else if (swipeDistance < -50) {
    nextImage(); // Свайп вліво - наступна картинка
  }
});

// Запуск початкового стану каруселі
updateCarousel();


// Reviews section

const swiper = new Swiper(".swiper", {
  // Optional parameters
  direction: "horizontal",
  loop: true,

  // Navigation arrows
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
});








function adjustContentBasedOnScreenSize() {
    // Для екранів шириною менше 768px
    if (window.innerWidth > 425) {
        const reviewContainers = document.querySelectorAll('.review-row');

        reviewContainers.forEach(function(reviewContainer) {
        	const reviewIdElement = reviewContainer.querySelector('.review-id');
	        const reviewId = reviewIdElement.getAttribute('data-review-id');

			var params = new URLSearchParams();
			params.append('reviewId', reviewId);

			const imageContainer = reviewContainer.querySelector('.review-images');

			fetch('/collections/get-images?' + params)
			    .then(response => response.json())
			    .then(data => {
			        var images = data.images;
			        imageContainer.innerHTML = '';

			        images.forEach(function(image) {
			        	var imageDiv = document.createElement('div');
			        	imageDiv.className = 'viewable-container';

			        	var imgElement = document.createElement('img');
			        	imgElement.className = 'viewable';
			        	imgElement.src = image.imageURL;
			        	imageDiv.appendChild(imgElement);
			        	imageContainer.appendChild(imageDiv);
			        })
			    })
			    .catch(error => {
			        console.log('Error:', error);
			    });
		});
	}
}

// Викликаємо функцію при завантаженні сторінки
adjustContentBasedOnScreenSize();

// Додаємо обробник події 'resize' для виклику функції при зміні розміру вікна
window.addEventListener('resize', adjustContentBasedOnScreenSize);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Перевіряємо, чи починається цей cookie із потрібного нам імені
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

		  	
