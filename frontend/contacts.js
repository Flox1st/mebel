document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('contactName').value;
    const email = document.getElementById('contactEmail').value;
    const subject = document.getElementById('contactSubject').value;
    const message = document.getElementById('contactMessage').value;

    // Простая валидация обязательных полей
    if (!name || !email || !subject || !message) {
        alert('Пожалуйста, заполните все обязательные поля (отмечены *)');
        return;
    }

    // В реальном проекте здесь был бы AJAX-запрос к серверу
    alert('Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.');

    // Очистка формы
    document.getElementById('contactForm').reset();
});