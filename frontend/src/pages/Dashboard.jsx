import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div style={styles.container}>
      <h2>Área restrita</h2>
      <p>
        Você está autenticado como <strong>{user.email}</strong> (ID: {user.id}).
      </p>
      <p>
        Esta página só é acessível com um JWT válido. Tente abrir
        <code> http://localhost:8000/me </code> em outra aba sem estar logado e
        veja a resposta 401.
      </p>
      <button onClick={logout} style={styles.button}>
        Sair
      </button>
    </div>
  );
}

const styles = {
  container: { maxWidth: 600, margin: "60px auto", padding: 20 },
  button: {
    padding: 10,
    fontSize: 14,
    cursor: "pointer",
    marginTop: 20,
  },
};