const API_URL = "http://localhost:8000";

export async function fetchHealth() {
  const res = await fetch(`${API_URL}/health`);
  if (!res.ok) throw new Error("API indisponible");
  return res.json();
}

export async function fetchResources() {
  const res = await fetch(`${API_URL}/resources/`);
  if (!res.ok) throw new Error("Impossible de charger les ressources");
  return res.json();
}

export async function searchResources(query) {
  const res = await fetch(
    `${API_URL}/resources/search/?q=${encodeURIComponent(query)}`
  );
  if (!res.ok) throw new Error("Erreur pendant la recherche");
  return res.json();
}

export async function createResource({ title, category, content }) {
  const res = await fetch(`${API_URL}/resources/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, category, content }),
  });
  if (!res.ok) throw new Error("Impossible de créer la ressource");
  return res.json();
}
