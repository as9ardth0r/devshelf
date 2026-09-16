import { useState } from "react";

export default function ResourceForm({ onCreated }) {
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("");
  const [content, setContent] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    setSubmitting(true);
    setError(null);
    try {
      await onCreated({ title, category: category || "Général", content });
      setTitle("");
      setCategory("");
      setContent("");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="resource-form" onSubmit={handleSubmit}>
      <h2>Ajouter une ressource</h2>
      <input
        type="text"
        placeholder="Titre"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Catégorie (ex: Backend, Design...)"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      />
      <textarea
        placeholder="Contenu..."
        rows={4}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        required
      />
      <button type="submit" disabled={submitting}>
        {submitting ? "Ajout en cours..." : "Ajouter"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
