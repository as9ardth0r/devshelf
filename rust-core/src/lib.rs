use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::collections::HashMap;

const STOPWORDS: &[&str] = &[
    "le", "la", "les", "de", "des", "du", "un", "une", "et", "en", "à",
    "au", "aux", "ce", "ces", "cet", "cette", "il", "elle", "ils", "elles",
    "je", "tu", "nous", "vous", "on", "que", "qui", "dans", "pour", "par",
    "sur", "est", "sont", "avec", "pas", "plus", "ou", "the", "a", "an",
    "and", "or", "of", "to", "in", "is", "for", "on", "with",
];

/// Découpe un texte en mots normalisés (minuscules, sans ponctuation).
fn tokenize(text: &str) -> Vec<String> {
    text.split(|c: char| !c.is_alphanumeric())
        .filter(|w| !w.is_empty())
        .map(|w| w.to_lowercase())
        .collect()
}

/// Analyse un contenu texte : nombre de mots, temps de lecture estimé,
/// et mots-clés les plus fréquents (hors mots vides).
///
/// Le calcul de fréquence sur un texte long est l'endroit où Rust apporte
/// un vrai gain de perf par rapport à une boucle Python équivalente.
#[pyfunction]
fn analyze_text(py: Python<'_>, content: &str) -> PyResult<PyObject> {
    let words = tokenize(content);
    let word_count = words.len();

    // ~200 mots/minute de lecture, arrondi au 1/10 de minute près
    let reading_time_minutes = ((word_count as f64 / 200.0) * 10.0).ceil() / 10.0;

    let mut freq: HashMap<String, usize> = HashMap::new();
    for w in &words {
        if w.len() > 3 && !STOPWORDS.contains(&w.as_str()) {
            *freq.entry(w.clone()).or_insert(0) += 1;
        }
    }
    let mut freq_vec: Vec<(String, usize)> = freq.into_iter().collect();
    freq_vec.sort_by(|a, b| b.1.cmp(&a.1).then(a.0.cmp(&b.0)));
    let keywords: Vec<String> = freq_vec.into_iter().take(5).map(|(w, _)| w).collect();

    let result = PyDict::new(py);
    result.set_item("word_count", word_count)?;
    result.set_item("reading_time_minutes", reading_time_minutes)?;
    result.set_item("keywords", keywords)?;
    Ok(result.into())
}

/// Score et classe une liste de ressources (id, titre, contenu) par
/// pertinence par rapport à une requête. Score = occurrences pondérées
/// (le titre compte 3x plus que le contenu), normalisé par la longueur.
/// Ne retourne que les ressources avec un score > 0, triées par pertinence.
#[pyfunction]
fn search_resources(
    query: &str,
    resources: Vec<(i64, String, String)>,
) -> PyResult<Vec<(i64, f64)>> {
    let query_terms = tokenize(query);
    if query_terms.is_empty() {
        return Ok(vec![]);
    }

    let mut scored: Vec<(i64, f64)> = resources
        .iter()
        .filter_map(|(id, title, content)| {
            let title_words = tokenize(title);
            let content_words = tokenize(content);
            let total_len = (title_words.len() + content_words.len()).max(1) as f64;

            let mut hits = 0.0_f64;
            for term in &query_terms {
                hits += title_words.iter().filter(|w| *w == term).count() as f64 * 3.0;
                hits += content_words.iter().filter(|w| *w == term).count() as f64;
            }

            if hits > 0.0 {
                Some((*id, hits / total_len.sqrt()))
            } else {
                None
            }
        })
        .collect();

    scored.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    Ok(scored)
}

#[pymodule]
fn rust_core(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(analyze_text, m)?)?;
    m.add_function(wrap_pyfunction!(search_resources, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize() {
        assert_eq!(tokenize("Bonjour, le monde!"), vec!["bonjour", "le", "monde"]);
    }

    #[test]
    fn test_search_ranks_title_higher() {
        let resources = vec![
            (1, "Rust performance".to_string(), "un article".to_string()),
            (2, "Autre sujet".to_string(), "parle de rust ici".to_string()),
        ];
        let results = search_resources("rust", resources).unwrap();
        assert_eq!(results[0].0, 1); // le match dans le titre doit remonter en premier
    }
}
