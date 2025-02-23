function scrollBooks(direction) {
    const container = document.querySelector('.book-container');
    const scrollAmount = container.offsetWidth; 

    container.scrollBy({
        left: direction * scrollAmount,
        behavior: 'smooth'
    });
}