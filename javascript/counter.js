let counter = 0;
let targetNumber = 100; // Replace with your desired target number
const speed = 3000;
const counterElement = document.getElementById("counter");
const container = document.querySelector(".container");

// Function to update the counter
function updateCounter() {
  const increment = (targetNumber / speed) * 10; // Calculate a smooth increment
  const interval = setInterval(() => {
    counter += increment;
    counterElement.textContent = Math.round(counter);
    if (counter >= targetNumber) {
      clearInterval(interval);
    }
  }, 10);
}

// Initialize Intersection Observer
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      updateCounter();
      observer.unobserve(container); // Stop observing once triggered
    }
  });
});

// Start observing the container
observer.observe(container);
