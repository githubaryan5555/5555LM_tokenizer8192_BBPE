from tokenizers import Tokenizer


TOKENIZER_FILE = "tokenizer.json"


def interactive_eval(tokenizer):
    print("=" * 70)
    print("INTERACTIVE TOKENIZER EVALUATION")
    print("=" * 70)
    print("Type text and press Enter.")
    print("Type :q to quit.")
    print()

    while True:
        try:
            text = input("TEXT > ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if text == ":q":
            break

        encoding = tokenizer.encode(text)

        ids = encoding.ids
        tokens = encoding.tokens

        decoded = tokenizer.decode(ids)

        print()
        print("-" * 70)

        print("ORIGINAL:")
        print(repr(text))

        print()
        print("TOKEN IDS:")
        print(ids)

        print()
        print("TOKENS:")

        for i, (token_id, token) in enumerate(zip(ids, tokens)):
            print(
                f"{i:4d} | "
                f"ID {token_id:4d} | "
                f"{token!r}"
            )

        print()
        print("DECODED:")
        print(repr(decoded))

        print()
        print(
            "ROUND TRIP:",
            "PASS ✅" if decoded == text else "FAIL ❌"
        )

        if decoded != text:
            print()
            print("Original bytes:")
            print(text.encode("utf-8"))

            print()
            print("Decoded bytes:")
            print(decoded.encode("utf-8"))

        print("-" * 70)
        print()


def main():
    tokenizer = Tokenizer.from_file(TOKENIZER_FILE)

    vocab = tokenizer.get_vocab()

    print(f"Loaded: {TOKENIZER_FILE}")
    print(f"Vocabulary size: {len(vocab)}")

    assert len(vocab) == 8192
    assert tokenizer.token_to_id("[-UNK-]") == 256
    assert tokenizer.token_to_id("[-BOS-]") == 257
    assert tokenizer.token_to_id("[-EOS-]") == 258

    print("Vocabulary checks: PASS")
    print()

    interactive_eval(tokenizer)


if __name__ == "__main__":
    main()
