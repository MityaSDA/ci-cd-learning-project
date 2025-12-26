/**
 * frontend/src/App.js
 *
 * Главный React-компонент приложения.
 *
 * Назначение:
 * - UI калькулятора
 * - Запросы к backend API
 * - Отображение результата и ошибок
 *
 * Архитектура:
 * - единая функция callApi
 * - backend URL вынесен в константу
 * - обработка ошибок на уровне UI
 */

import React, { useState } from "react";

// ============================================================
// 1. URL backend API
// ============================================================
//
// Backend задеплоен на Render.
// Все API-эндпоинты имеют префикс /api
//
const API_BASE_URL = "https://myapp-latest-b5gs.onrender.com/api";

// ============================================================
// 2. Основной компонент
// ============================================================

function App() {

  // ----------------------------------------------------------
  // React state
  // ----------------------------------------------------------
  // result — результат вычисления
  // error  — текст ошибки (если запрос не удался)
  //
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // ----------------------------------------------------------
  // Универсальная функция вызова API
  // ----------------------------------------------------------
  //
  // endpoint — строка вида:
  //   "/add?a=2&b=3"
  //
  const callApi = async (endpoint) => {
    // При новом запросе сбрасываем старую ошибку
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);

      // Если backend вернул НЕ 200–299
      if (!response.ok) {
        throw new Error("HTTP error");
      }

      const json = await response.json();

      // Если backend вернул success=false
      if (!json.success) {
        throw new Error(json.error);
      }

      // Успех → обновляем результат
      setResult(json.data.result);

    } catch (err) {
      console.error("API error:", err);
      setError("Ошибка запроса к API");
    }
  };

  // ==========================================================
  // 3. UI
  // ==========================================================

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>MyApp Calculator</h1>

      {/* Кнопка сложения */}
      <button onClick={() => callApi("/add?a=2&b=3")}>
        Add 2 + 3
      </button>

      {/* Кнопка умножения */}
      <button
        onClick={() => callApi("/multiply?a=4&b=5")}
        style={{ marginLeft: "10px" }}
      >
        Multiply 4 × 5
      </button>

      {/* Результат */}
      <h2 style={{ marginTop: "20px" }}>
        Result: {result !== null ? result : "—"}
      </h2>

      {/* Ошибка */}
      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}
    </div>
  );
}

export default App;
