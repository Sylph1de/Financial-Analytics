mkdir -p ~/.streamlit/

echo '\
[runner]\n\
fastReruns = true\n\
\n\
[theme]\n\
base="dark"\n\
primaryColor = "violet"\n\
\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
' > ~/.streamlit/config.toml
