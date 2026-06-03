import axios from "axios";

// Em produção (Vercel), VITE_API_URL aponta para o backend no Render.
// Localmente, se a variável não existir, cai no backend local :8000.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// Interceptor de REQUEST: adiciona o token em toda requisição
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor de RESPONSE: trata 401 globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token inválido ou expirado: limpa e força login
      localStorage.removeItem("access_token");
      // Só redireciona se NÃO estiver tentando logar
      if (!window.location.pathname.startsWith("/login")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;