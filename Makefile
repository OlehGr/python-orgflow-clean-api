default: lint

lint:
	uv run ruff check --fix .
	uv run -m ty check .
	$(MAKE) update-example-env


update-example-env:
	@if [ ! -f .env ]; then \
		echo ".env file not found"; \
		exit 1; \
	fi

	@echo "Generating example.env from .env..."

	@awk '\
	BEGIN { FS="=" } \
	/^[[:space:]]*#/ { print $$0; next } \
	/^[[:space:]]*$$/ { print $$0; next } \
	/=/ { \
		key=$$1; \
		sub(/[[:space:]]+$$/, "", key); \
		print key "="; \
		next \
	} \
	{ print $$0 } \
	' .env > example.env

	@echo "example.env updated."
