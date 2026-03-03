// auth.js - МАКСИМАЛЬНО ПОДРОБНАЯ ВЕРСИЯ

console.log('=== auth.js загружен ===');

async function handleLogin(event) {
    console.log('=== handleLogin НАЧАЛО ===');
    console.log('Событие:', event);
    
    // Предотвращаем отправку формы
    if (event) {
        event.preventDefault();
        console.log('event.preventDefault() выполнен');
    }
    
    // Получаем значения полей
    console.log('Поиск элементов формы...');
    const usernameInput = document.getElementById('loginInput');
    const passwordInput = document.getElementById('passwordInput');
    
    console.log('loginInput найден:', usernameInput ? 'да' : 'нет');
    console.log('passwordInput найден:', passwordInput ? 'да' : 'нет');
    
    if (!usernameInput || !passwordInput) {
        console.error('Элементы формы не найдены!');
        alert('Ошибка: форма входа не найдена');
        return;
    }
    
    const username = usernameInput.value.trim();
    const password = passwordInput.value;
    
    console.log('Логин (username):', username);
    console.log('Пароль введен:', password ? 'да (длина: ' + password.length + ')' : 'нет');
    
    if (!username || !password) {
        console.log('Валидация не пройдена: пустые поля');
        alert('Заполните все поля');
        return;
    }
    
    console.log('Валидация пройдена, отправка запроса...');
    
    try {
        // Отправляем запрос
        console.log('Создание FormData...');
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        console.log('FormData создана, поля добавлены');
        
        console.log('Отправка fetch запроса к /api/login...');
        const response = await fetch('/api/login', {
            method: 'POST',
            body: formData
        });
        
        console.log('Ответ получен, статус:', response.status);
        console.log('Статус текстом:', response.statusText);
        
        console.log('Парсинг JSON ответа...');
        const result = await response.json();
        console.log('JSON распарсен, результат:', result);
        
        console.log('Проверка result.success =', result.success);
        
        if (result.success) {
            console.log('=== СОХРАНЕНИЕ ДАННЫХ ===');
            
            // Сохраняем токен
            console.log('1. Сохраняем authToken =', result.access_token);
            localStorage.setItem('authToken', result.access_token);
            console.log('   authToken сохранен, проверка:', localStorage.getItem('authToken'));
            
            // Сохраняем пользователя
            console.log('2. Сохраняем currentUser =', result.user);
            localStorage.setItem('currentUser', JSON.stringify(result.user));
            console.log('   currentUser сохранен, проверка:', localStorage.getItem('currentUser'));
            
            // Сохраняем флаг авторизации
            console.log('3. Сохраняем userLoggedIn = true');
            localStorage.setItem('userLoggedIn', 'true');
            console.log('   userLoggedIn сохранен, проверка:', localStorage.getItem('userLoggedIn'));
            
            console.log('=== ВСЕ ДАННЫЕ СОХРАНЕНЫ ===');
            
            // Показываем всё содержимое localStorage
            console.log('=== СОДЕРЖИМОЕ LOCALSTORAGE ПОСЛЕ СОХРАНЕНИЯ ===');
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                const value = localStorage.getItem(key);
                console.log(key + ':', value);
            }
            console.log('=== КОНЕЦ СОДЕРЖИМОГО ===');
            
            alert('✅ Вход выполнен успешно!');
            
            console.log('Перезагрузка страницы через 1 секунду...');
            setTimeout(() => {
                console.log('Перезагрузка страницы...');
                window.location.reload();
            }, 1000);
            
        } else {
            console.log('Ошибка входа от сервера:', result.message);
            alert('❌ ' + (result.message || 'Ошибка при входе'));
        }
        
    } catch (error) {
        console.error('!!! ПЕРЕХВАЧЕНА ОШИБКА !!!');
        console.error('Тип ошибки:', error.name);
        console.error('Сообщение ошибки:', error.message);
        console.error('Стек ошибки:', error.stack);
        alert('Ошибка соединения с сервером: ' + error.message);
    }
    
    console.log('=== handleLogin КОНЕЦ ===');
}

function handleLogout() {
    console.log('=== handleLogout ===');
    console.log('Очистка localStorage...');
    
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('userLoggedIn');
    
    console.log('localStorage очищен');
    console.log('Проверка после очистки:');
    console.log('authToken:', localStorage.getItem('authToken'));
    console.log('currentUser:', localStorage.getItem('currentUser'));
    console.log('userLoggedIn:', localStorage.getItem('userLoggedIn'));
    
    console.log('Переход на главную страницу...');
    window.location.href = '/';
}

function updateAuthUI() {
    console.log('=== updateAuthUI ===');
    
    const loginForm = document.querySelector('.login-form');
    const userView = document.getElementById('userView');
    const userGreeting = document.getElementById('userGreeting');
    
    console.log('loginForm найден:', loginForm ? 'да' : 'нет');
    console.log('userView найден:', userView ? 'да' : 'нет');
    console.log('userGreeting найден:', userGreeting ? 'да' : 'нет');
    
    if (!loginForm || !userView) {
        console.log('Элементы UI не найдены, выход');
        return;
    }
    
    // Получаем данные
    const token = localStorage.getItem('authToken');
    const userDataStr = localStorage.getItem('currentUser');
    const loggedIn = localStorage.getItem('userLoggedIn');
    
    console.log('Текущий токен:', token);
    console.log('Текущий userData:', userDataStr);
    console.log('Текущий loggedIn:', loggedIn);
    
    if (token && userDataStr && loggedIn === 'true') {
        console.log('Пользователь авторизован, показываем userView');
        try {
            const userData = JSON.parse(userDataStr);
            console.log('Распарсенные данные пользователя:', userData);
            
            loginForm.style.display = 'none';
            userView.style.display = 'block';
            
            if (userGreeting) {
                userGreeting.textContent = 'Привет, ' + userData.username + '!';
                console.log('Приветствие установлено');
            }
        } catch (e) {
            console.error('Ошибка парсинга userData:', e);
        }
    } else {
        console.log('Пользователь не авторизован, показываем loginForm');
        loginForm.style.display = 'flex';
        userView.style.display = 'none';
    }
}

// Выполняется при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOMContentLoaded в auth.js ===');
    console.log('Текущий URL:', window.location.href);
    console.log('Текущий токен:', localStorage.getItem('authToken'));
    console.log('Текущий userLoggedIn:', localStorage.getItem('userLoggedIn'));
    console.log('Текущий currentUser:', localStorage.getItem('currentUser'));
    
    updateAuthUI();
    
    // Добавляем обработчик на форму входа
    const loginButton = document.querySelector('.login-form button');
    if (loginButton) {
        console.log('Кнопка входа найдена, добавляем обработчик');
        
        // Удаляем старый обработчик если был
        loginButton.onclick = null;
        
        // Добавляем новый
        loginButton.onclick = function(e) {
            console.log('Клик по кнопке входа');
            handleLogin(e);
            return false;
        };
        
        console.log('Обработчик добавлен');
    } else {
        console.log('Кнопка входа не найдена');
    }
    
    // Добавляем обработчик на форму
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        console.log('Форма входа найдена, добавляем обработчик submit');
        loginForm.addEventListener('submit', function(e) {
            console.log('Событие submit на форме');
            handleLogin(e);
        });
    }
});

console.log('=== auth.js полностью загружен, функции определены ===');
console.log('handleLogin определена:', typeof handleLogin === 'function');
console.log('handleLogout определена:', typeof handleLogout === 'function');

// Делаем функции доступными глобально
window.handleLogin = handleLogin;
window.handleLogout = handleLogout;