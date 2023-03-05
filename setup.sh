mkdir -p ~/.streamlit/

echo "\
[runner]
fastReruns = true\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false" > ~/.streamlit/config.toml
