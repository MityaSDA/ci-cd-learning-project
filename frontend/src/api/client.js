// Базовый URL backend API
// Локально можно менять на http://localhost:5000
const API_BASE_URL = "https://myapp-latest-b5gs.onrender.com";

// Проверка состояния сервиса
export async function getHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}

// Сложение
export async function add(a, b) {
  const response = await fetch(
    `${API_BASE_URL}/add?a=${a}&b=${b}`
  );
  return response.json();
}

// Умножение
export async function multiply(a, b) {
  const response = await fetch(
    `${API_BASE_URL}/multiply?a=${a}&b=${b}`
  );
  return response.json();
}
