document.addEventListener("DOMContentLoaded", () => {
  const slider = document.querySelector("[data-slider]");
  if (!slider) return;

  const slides = Array.from(slider.querySelectorAll("[data-slide]"));
  const prevButton = slider.querySelector("[data-prev]");
  const nextButton = slider.querySelector("[data-next]");
  const dotsContainer = slider.querySelector("[data-dots]");

  let activeIndex = slides.findIndex((slide) => slide.classList.contains("is-active"));
  if (activeIndex === -1) {
    activeIndex = 0;
    slides[0]?.classList.add("is-active");
  }

  const buildDots = () => {
    slides.forEach((_, index) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.setAttribute("aria-label", `Go to slide ${index + 1}`);
      dot.addEventListener("click", () => goToSlide(index));
      dotsContainer?.appendChild(dot);
    });
  };

  const updateActive = () => {
    slides.forEach((slide, index) => {
      slide.classList.toggle("is-active", index === activeIndex);
    });
    if (dotsContainer) {
      dotsContainer.querySelectorAll("button").forEach((dot, index) => {
        dot.setAttribute("aria-current", index === activeIndex ? "true" : "false");
      });
    }
  };

  const goToSlide = (index) => {
    activeIndex = (index + slides.length) % slides.length;
    updateActive();
  };

  const goNext = () => goToSlide(activeIndex + 1);
  const goPrev = () => goToSlide(activeIndex - 1);

  buildDots();
  updateActive();

  prevButton?.addEventListener("click", goPrev);
  nextButton?.addEventListener("click", goNext);

  let autoSlideInterval = window.setInterval(goNext, 6000);

  slider.addEventListener("mouseenter", () => window.clearInterval(autoSlideInterval));
  slider.addEventListener("mouseleave", () => {
    autoSlideInterval = window.setInterval(goNext, 6000);
  });
});



