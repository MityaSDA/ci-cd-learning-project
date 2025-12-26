/**
 * frontend/src/App.js
 *
 * React UI (учебный калькулятор) с максимально прозрачной логикой:
 *
 * - единая функция callApi для всех операций
 * - строгая работа с унифицированным API backend
 * - корректная обработка success / error
 * - подробные комментарии ПОЧЕМУ именно так
 *
 * Backend API (АКТУАЛЬНЫЙ КОНТРАКТ):
 * --------------------------------
 * УСПЕХ:
 * {
 *   "success": true,
 *   "data": {
 *     "operation": "add",
 *     "a": 2,
 *     "b": 3,
 *     "result": 5
 *   },
 *   "error": null
 * }
 *
 * ОШИБКА:
 * {
 *   "success": false,
 *   "data": null,
 *   "error": "Error message"
 * }
 *
 * ВАЖНО:
 * ------
 * Раньше frontend ожидал:
 *   response.result
 *
 * Теперь ПРАВИЛЬНО:
 *   response.data.result
 */

import React, { useMemo, useState } from "react";

/* ============================================================
 * 1) API BASE URL
 * ============================================================
 *
 * Если REACT_APP_API_BASE задан в .env:
 *   REACT_APP_API_BASE=https://myapp-latest-xxxx.onrender.com
 *
 * Тогда запросы пойдут на:
 *   https://myapp-latest-xxxx.onrender.com/api/add
 *
 * Если переменная НЕ задана:
 *   frontend использует относительные пути /api/*
 *   (подходит, если фронт и бэк за одним доменом)
 */
const API_BASE_FROM_ENV = process.env.REACT_APP_API_BASE || "";

/**
 * Аккуратно склеивает base + path,
 * чтобы не было двойных слэшей.
 */
function joinUrl(base, path) {
  if (!base) return path;
  return base.replace(/\/+$/, "") + path;
}

export default function App() {
  /* ============================================================
   * 2) STATE
   * ============================================================
   */
  const [result, setResult] = useState(null);   // число или null
  const [error, setError] = useState("");       // строка ошибки
  const [loading, setLoading] = useState(false);

  // Числа для примера (потом легко заменить на input’ы)
  const a = 2;
  const b = 3;

  // Базовый URL backend (фиксируется один раз)
  const apiBase = useMemo(() => API_BASE_FROM_ENV, []);

  /* ============================================================
   * 3) ЕДИНАЯ ФУНКЦИЯ ВЫЗОВА API
   * ============================================================
   */
  async function callApi(operation, aValue, bValue) {
    // Перед новым запросом сбрасываем состояние
    setError("");
    setResult(null);
    setLoading(true);

    try {
      // Формируем путь API
      // /api/add?a=2&b=3
      const path = `/api/${operation}?a=${encodeURIComponent(
        aValue
      )}&b=${encodeURIComponent(bValue)}`;

      const url = joinUrl(apiBase, path);

      // Делаем HTTP-запрос
      const response = await fetch(url, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });

      // Пытаемся распарсить JSON (даже если статус не 200)
      const json = await response.json().catch(() => null);

      // --------------------------------------------------------
      // 1) HTTP-ошибка (не 2xx)
      // --------------------------------------------------------
      if (!response.ok) {
        // Backend всегда кладёт сообщение в error
        const message =
          json?.error ||
          `HTTP ${response.status} (${response.statusText})`;

        throw new Error(message);
      }

      // --------------------------------------------------------
      // 2) API-level ошибка (success = false)
      // --------------------------------------------------------
      if (!json || json.success !== true) {
        const message = json?.error || "API returned success=false";
        throw new Error(message);
      }

      // --------------------------------------------------------
      // 3) Проверяем формат данных
      // --------------------------------------------------------
      const apiResult = json?.data?.result;

      if (typeof apiResult !== "number") {
        throw new Error(
          "Invalid API response: data.result is missing or not a number"
        );
      }

      // Всё ок — сохраняем результат
      setResult(apiResult);
    } catch (err) {
      console.error("API error:", err);
      setError(err.message || "Ошибка запроса к API");
    } finally {
      setLoading(false);
    }
  }

  /* ============================================================
   * 4) UI
   * ============================================================
   */
  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: 32 }}>
      <h1>MyApp Calculator</h1>

      {/* Показываем, куда реально идут запросы */}
      <p style={{ color: "#555" }}>
        <b>API base:</b>{" "}
        {apiBase ? apiBase : "(same-origin → /api/*)"}
      </p>

      <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
        <button
          onClick={() => callApi("add", a, b)}
          disabled={loading}
        >
          Add {a} + {b}
        </button>

        <button
          onClick={() => callApi("multiply", 4, 5)}
          disabled={loading}
        >
          Multiply 4 × 5
        </button>

        {/*
        <button
          onClick={() => callApi("divide", 10, 2)}
          disabled={loading}
        >
          Divide 10 / 2
        </button>
        */}
      </div>

      <h2 style={{ marginTop: 24 }}>
        Result:{" "}
        {loading ? "Loading..." : result === null ? "—" : result}
      </h2>

      {error && (
        <p style={{ color: "red", fontWeight: "bold" }}>{error}</p>
      )}

      {/* Объяснение типичных проблем */}
      <div style={{ marginTop: 24, color: "#666", maxWidth: 900 }}>
        <p>
          <b>Если снова видишь ошибку:</b>
        </p>
        <ul>
          <li>
            Проверь, что backend реально обновился на Render
            (CI должен быть зелёным).
          </li>
          <li>
            Проверь контракт API: <code>data.result</code>, а не
            <code>result</code>.
          </li>
          <li>
            Проверь CORS в <code>backend/app.py</code>.
          </li>
        </ul>
      </div>
    </div>
  );
}
