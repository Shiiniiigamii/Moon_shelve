document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector(".search-bar input[name='q']");
    let suggestionsBox = document.getElementById("suggestions");

    if (!suggestionsBox) {
        suggestionsBox = document.createElement("div");
        suggestionsBox.id = "suggestions";
        searchInput.parentNode.appendChild(suggestionsBox);
    }

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim();
        if (query.length > 1) {
            fetch(`/search_suggestions/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = "";
                    suggestionsBox.style.display = "block"; // Показываем подсказки
                    suggestionsBox.style.position = "absolute"; // Фиксируем позицию
                    suggestionsBox.style.left = `${searchInput.offsetLeft}px`; // Выравнивание
                    suggestionsBox.style.top = `${searchInput.offsetTop + searchInput.offsetHeight + 10}px`; // Под input с дополнительным отступом

                    data.forEach(book => {
                        const suggestionItem = document.createElement("div");
                        suggestionItem.textContent = `${book.title} - ${book.author}`;
                        suggestionItem.classList.add("suggestion-item");
                        suggestionItem.addEventListener("click", function () {
                            searchInput.value = book.title;
                            suggestionsBox.style.display = "none"; // Скрываем после выбора
                        });
                        suggestionsBox.appendChild(suggestionItem);
                    });
                })
                .catch(error => console.error("Ошибка загрузки данных:", error));
        } else {
            suggestionsBox.style.display = "none";
        }
    });

    document.addEventListener("click", function (event) {
        if (!searchInput.contains(event.target) && !suggestionsBox.contains(event.target)) {
            suggestionsBox.style.display = "none"; // Скрываем при клике вне подсказок
        }
    });
});
