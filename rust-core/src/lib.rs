pub fn process_data(input: &str) -> String {
    format!("Processed by Rust core: {}", input)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process_data() {
        let result = process_data("test");
        assert_eq!(result, "Processed by Rust core: test");
    }
}
