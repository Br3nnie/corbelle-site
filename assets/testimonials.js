const dialog = document.querySelector('.testimonial-dialog');
const dialogImage = dialog.querySelector('img');
const dialogTitle = dialog.querySelector('#testimonial-dialog-title');
const closeButton = dialog.querySelector('.testimonial-dialog-close');

document.querySelectorAll('.testimonial-card').forEach((card) => {
  card.addEventListener('click', () => {
    const name = card.dataset.testimonialName;
    dialogImage.src = card.dataset.testimonialSrc;
    dialogImage.alt = `Testimonial from ${name} about working with Brendan`;
    dialogTitle.textContent = `${name} · Testimonial`;
    dialog.showModal();
  });
});

closeButton.addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => {
  if (event.target === dialog) dialog.close();
});

