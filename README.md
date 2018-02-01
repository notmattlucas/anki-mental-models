docker build -f src/Dockerfile -t amm:latest src/ && docker run -v .:/app/target amm:latest
