"""Command-line utility to list available models."""


from ENHANCER.models import MODEL_PROVIDERS, get_all_models


def main() -> None:
    """List all available models grouped by provider."""
    print("\nENHANCER - Available AI Models")
    print("=" * 60)

    for provider, models in MODEL_PROVIDERS.items():
        print(f"\n{provider.upper()} Models:")
        print("-" * 40)
        for model in models:
            print(f"  - {model}")

    all_models = get_all_models()
    print(f"\n{'=' * 60}")
    print(f"Total: {len(all_models)} models available")
    print()


if __name__ == "__main__":
    main()
