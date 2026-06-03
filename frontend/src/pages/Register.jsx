import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await register(email, password);
      navigate("/"); // após registrar (e logar), vai para dashboard
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(detail || "Erro ao registrar");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Criar conta</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={styles.input}
        />
        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
          style={styles.input}
        />
        <button type="submit" disabled={submitting} style={styles.button}>
          {submitting ? "Registrando..." : "Registrar"}
        </button>
        {error && <p style={styles.error}>{error}</p>}
      </form>
      <p>
        Já tem conta? <Link to="/login">Entrar</Link>
      </p>
    </div>
  );
}

const styles = {
  container: { maxWidth: 360, margin: "60px auto", padding: 20 },
  form: { display: "flex", flexDirection: "column", gap: 12 },
  input: { padding: 8, fontSize: 14 },
  button: { padding: 10, fontSize: 14, cursor: "pointer" },
  error: { color: "crimson", margin: 0 },
};