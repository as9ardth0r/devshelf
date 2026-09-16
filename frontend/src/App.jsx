import { useEffect, useState, useCallback } from "react";
import { fetchHealth, fetchResources, searchResources, createResource } from "./api";
import ResourceForm from "./ResourceForm";
import ResourceCard from "./ResourceCard";
import "./App.css";

export default function App() {
  const [apiStatus, setApiStatus] = useState("checking");
  const [resources, setResources] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadResources = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = query.trim()
        ? await searchResources(query.trim())
        : await fetchResources();
      setResources(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    fetchHealth()
      .then(() => setApiStatus("online"))
      .catch(() => setApiStatus("offline"));
  }, []);

  useEffect(() => {
    loadResources();
  }, [loadResources]);

  async function handleCreate(payload) {
    await createResource(payload);
    await loadResources();
  }

  return (
    <div className="app">
      <header>
        <h1>DevShelf</h1>
        <p>Espace de centralisation technique et créatif</p>
        <span className={`status-pill ${apiStatus}`}>
          API : {apiStatus === "online" ? "en ligne" : apiStatus === "offline" ? "hors ligne" : "..."}
        </span>
      </header>

      <main>
        <section className="card">
          <ResourceForm onCreated={handleCreate} />
        </section>

        <section className="card">
          <h2>Ressources</h2>
          <input
            type="search"
            className="search-input"
            placeholder="Rechercher (classement calculé côté Rust)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          {loading && <p>Chargement...</p>}
          {error && <p className="error">{error}</p>}
          {!loading && !error && resources.length === 0 && (
            <p>Aucune ressource pour le moment.</p>
          )}

          <div className="resource-list">
            {resources.map((r) => (
              <ResourceCard key={r.id} resource={r} />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
