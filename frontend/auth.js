// auth.js - общий скрипт для всех страниц

// Функция входа
async function handleLogin(event) {
    if (event) event.preventDefault();
    
    // Находим поля формы
    const loginForm = event ? event.target.closest('.login-form') : document.querySelector('.login-form');
    if (!loginForm) return;
    
    // Ищем поля ввода
    const usernameInput = loginForm.querySelector('input[type="text"], input[name="username"], #loginInput');
    const passwordInput = loginForm.querySelector('input[type="password"], input[name="password"], #passwordInput');
    
    if (!usernameInput || !passwordInput) {
        alert('Форма входа не найдена');
        return;
    }
    
    const username = usernameInput.value.trim();
    const password = passwordInput.value;
    
    console.log('Login attempt:', { username, passwordLength: password.length });
    
    // Валидация
    if (!username || !password) {
        alert('Пожалуйста, заполните все поля');
        return;
    }
    
    try {
        // Отправляем данные
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch('/api/login', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        console.log('Login result:', result);
        
        if (result.success) {
            // Сохраняем данные
            localStorage.setItem('currentUser', JSON.stringify(result.user));
            localStorage.setItem('userLoggedIn', 'true');
            
            // Обновляем UI
            updateAuthUI();
            
            // Очищаем поля
            usernameInput.value = '';
            passwordInput.value = '';
            
            // Показываем уведомление
            alert('✅ Вход выполнен успешно!');
        } else {
            alert('❌ ' + result.message);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('🚫 Ошибка соединения с сервером');
    }
}

// Функция выхода
function handleLogout() {
    localStorage.removeItem('currentUser');
    localStorage.setItem('userLoggedIn', 'false');
    updateAuthUI();
    // Перенаправляем на главную
    window.location.href = '/';
}

// Обновление интерфейса
function updateAuthUI() {
    const loginForm = document.querySelector('.login-form');
    const userView = document.getElementById('userView');
    const userGreeting = document.getElementById('userGreeting');

    if (!loginForm || !userView) return;

    const userData = getCurrentUser();

    if (userData) {
        loginForm.style.display = 'none';
        userView.style.display = 'block';
        if (userGreeting) {
            userGreeting.textContent = `Привет, ${userData.username}!`;
        }
    } else {
        loginForm.style.display = 'flex';
        userView.style.display = 'none';
    }
}

// Получение текущего пользователя
function getCurrentUser() {
    const userStr = localStorage.getItem('currentUser');
    if (!userStr) return null;
    
    try {
        return JSON.parse(userStr);
    } catch (e) {
        console.error('Error parsing user data:', e);
        return null;
    }
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    console.log('Auth script loaded');
    
    // Находим форму
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        // Добавляем обработчик если его нет
        if (!loginForm.hasAttribute('data-handler-added')) {
            // Ищем кнопку входа
            const loginButton = loginForm.querySelector('button[onclick*="handleLogin"], button:not([onclick])');
            
            if (loginButton) {
                // Заменяем onclick
                loginButton.onclick = function(e) {
                    handleLogin(e);
                    return false;
                };
            }
            
            // Также добавляем обработчик на саму форму
            loginForm.addEventListener('submit', function(e) {
                e.preventDefault();
                handleLogin(e);
            });
            
            loginForm.setAttribute('data-handler-added', 'true');
        }
    }
    
    // Обновляем UI
    updateAuthUI();
});

// Делаем функции доступными глобально
window.handleLogin = handleLogin;
window.handleLogout = handleLogout;
window.updateAuthUI = updateAuthUI;