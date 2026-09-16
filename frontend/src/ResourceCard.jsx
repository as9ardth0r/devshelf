export default function ResourceCard({ resource }) {
  return (
    <article className="resource-card">
      <div className="resource-card-header">
        <h3>{resource.title}</h3>
        <span className="badge">{resource.category}</span>
      </div>
      <p className="resource-content">{resource.content}</p>
      <div className="resource-meta">
        <span>{resource.word_count} mots</span>
        <span>·</span>
        <span>{resource.reading_time_minutes} min de lecture</span>
      </div>
      {resource.keywords.length > 0 && (
        <div className="keywords">
          {resource.keywords.map((kw) => (
            <span key={kw} className="keyword">
              #{kw}
            </span>
          ))}
        </div>
      )}
    </article>
  );
}
