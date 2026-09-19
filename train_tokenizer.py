
import json
import os
import tempfile
from pathlib import Path

from tokenizers import Tokenizer, models, pre_tokenizers, decoders, trainers


# ============================================================
# Configuration
# ============================================================

INPUT_FILE = "fineweb_sample.txt"

VOCAB_SIZE = 8192

SPECIAL_TOKENS = {
    "unk_token": "[-UNK-]",
    "bos_token": "[-BOS-]",
    "eos_token": "[-EOS-]",
}

BYTE_VOCAB_SIZE = 256
SPECIAL_START = 256
LEARNED_START = 259

TRAIN_RATIO = 0.90

TOKENIZER_FILE = "tokenizer.json"
CONFIG_FILE = "tokenizer_config.json"


# ============================================================
# Build byte-level BPE
# ============================================================

def build_tokenizer(train_file):
    tokenizer = Tokenizer(
        models.BPE(
            unk_token=SPECIAL_TOKENS["unk_token"]
        )
    )

    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(
        add_prefix_space=False,
        use_regex=True,
    )

    tokenizer.decoder = decoders.ByteLevel()

    trainer = trainers.BpeTrainer(
        vocab_size=VOCAB_SIZE - 3,
        min_frequency=2,
        show_progress=True,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
        special_tokens=[],
    )

    tokenizer.train(
        [train_file],
        trainer=trainer,
    )

    return tokenizer


# ============================================================
# Split data into train/eval
# ============================================================

def make_train_eval_files(path):
    data = Path(path).read_bytes()

    split = int(len(data) * TRAIN_RATIO)

    train_data = data[:split]
    eval_data = data[split:]

    tmpdir = tempfile.mkdtemp(prefix="bbpe_")

    train_file = os.path.join(tmpdir, "train.txt")
    eval_file = os.path.join(tmpdir, "eval.txt")

    Path(train_file).write_bytes(train_data)
    Path(eval_file).write_bytes(eval_data)

    return train_file, eval_file


# ============================================================
# Remap vocabulary
#
# 0..255   = bytes
# 256      = [-UNK-]
# 257      = [-BOS-]
# 258      = [-EOS-]
# 259..    = learned BPE tokens
# ============================================================

def remap_vocab(tokenizer_json):
    vocab = tokenizer_json["model"]["vocab"]

    byte_tokens = {}
    learned_tokens = {}

    for token, token_id in vocab.items():
        if token_id < BYTE_VOCAB_SIZE:
            byte_tokens[token] = token_id
        else:
            learned_tokens[token] = token_id

    # Verify the trainer created the expected 256 byte tokens.
    byte_ids = sorted(byte_tokens.values())

    if byte_ids != list(range(256)):
        raise RuntimeError(
            "Byte vocabulary does not occupy IDs 0..255."
        )

    new_vocab = {}

    # Preserve byte IDs exactly.
    for token, token_id in byte_tokens.items():
        new_vocab[token] = token_id

    # Put special tokens exactly at 256..258.
    new_vocab[SPECIAL_TOKENS["unk_token"]] = 256
    new_vocab[SPECIAL_TOKENS["bos_token"]] = 257
    new_vocab[SPECIAL_TOKENS["eos_token"]] = 258

    # Shift every learned token by +3.
    for token, old_id in learned_tokens.items():
        new_vocab[token] = old_id + 3

    tokenizer_json["model"]["vocab"] = new_vocab

    # Make sure there are exactly 8192 tokens.
    if len(new_vocab) != VOCAB_SIZE:
        raise RuntimeError(
            f"Expected {VOCAB_SIZE} vocabulary entries, "
            f"got {len(new_vocab)}."
        )

    # Add special tokens to the tokenizer itself.
    tokenizer_json["added_tokens"] = [
        {
            "id": 256,
            "content": "[-UNK-]",
            "single_word": False,
            "lstrip": False,
            "rstrip": False,
            "normalized": False,
            "special": True,
        },
        {
            "id": 257,
            "content": "[-BOS-]",
            "single_word": False,
            "lstrip": False,
            "rstrip": False,
            "normalized": False,
            "special": True,
        },
        {
            "id": 258,
            "content": "[-EOS-]",
            "single_word": False,
            "lstrip": False,
            "rstrip": False,
            "normalized": False,
            "special": True,
        },
    ]

    return tokenizer_json


# ============================================================
# Evaluation
# ============================================================

def evaluate(tokenizer, eval_file):
    data = Path(eval_file).read_text(
        encoding="utf-8",
        errors="replace",
    )

    encoding = tokenizer.encode(data)

    ids = encoding.ids
    tokens = encoding.tokens

    total_chars = len(data)
    total_bytes = len(data.encode("utf-8"))
    total_tokens = len(ids)

    special_ids = {
        256: "[-UNK-]",
        257: "[-BOS-]",
        258: "[-EOS-]",
    }

    special_counts = {
        name: ids.count(token_id)
        for token_id, name in special_ids.items()
    }

    unknown_count = ids.count(256)

    decoded = tokenizer.decode(ids)

    # ByteLevel decoding should reconstruct the original text
    # for ordinary UTF-8 text.
    roundtrip_ok = decoded == data

    print()
    print("=" * 60)
    print("TOKENIZER EVALUATION")
    print("=" * 60)

    print(f"Evaluation characters : {total_chars:,}")
    print(f"Evaluation bytes      : {total_bytes:,}")
    print(f"Generated tokens      : {total_tokens:,}")

    if total_tokens:
        print(
            f"Bytes / token         : "
            f"{total_bytes / total_tokens:.4f}"
        )

        print(
            f"Characters / token    : "
            f"{total_chars / total_tokens:.4f}"
        )

    print(f"UNK tokens            : {unknown_count:,}")
    print(
        f"UNK rate              : "
        f"{unknown_count / max(total_tokens, 1) * 100:.6f}%"
    )

    print()
    print("Special-token counts:")

    for name, count in special_counts.items():
        print(f"  {name:8s}: {count:,}")

    print()
    print(f"Round-trip decode     : {'PASS' if roundtrip_ok else 'FAIL'}")

    # Check every byte ID.
    print()
    print("Byte-ID check:")

    byte_check = True

    for byte_id in range(256):
        token = tokenizer.id_to_token(byte_id)

        if token is None:
            byte_check = False
            break

    print(
        f"  IDs 0..255 present  : "
        f"{'PASS' if byte_check else 'FAIL'}"
    )

    print()
    print("Special-ID check:")

    special_check = (
        tokenizer.token_to_id("[-UNK-]") == 256
        and tokenizer.token_to_id("[-BOS-]") == 257
        and tokenizer.token_to_id("[-EOS-]") == 258
    )

    print(
        f"  256..258 correct    : "
        f"{'PASS' if special_check else 'FAIL'}"
    )

    print()
    print("Sample encoding:")

    sample = data[:500]
    sample_encoding = tokenizer.encode(sample)

    print("TEXT:")
    print(repr(sample[:200]))

    print()
    print("TOKENS:")
    print(sample_encoding.tokens[:80])

    print()
    print("IDS:")
    print(sample_encoding.ids[:80])

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Could not find {INPUT_FILE}"
        )

    print("=" * 60)
    print("8192-VOCAB BYTE-LEVEL BPE TRAINER")
    print("=" * 60)

    print(f"Input file : {INPUT_FILE}")
    print(f"Target vocab : {VOCAB_SIZE}")

    print()
    print("Vocabulary layout:")
    print("  0..255      = 256 byte tokens")
    print("  256         = [-UNK-]")
    print("  257         = [-BOS-]")
    print("  258         = [-EOS-]")
    print("  259..8191   = learned BPE tokens")
    print()

    train_file, eval_file = make_train_eval_files(
        INPUT_FILE
    )

    print("Training split:")
    print(f"  {train_file}")

    print()
    print("Evaluation split:")
    print(f"  {eval_file}")

    print()
    print("Training BPE...")

    tokenizer = build_tokenizer(train_file)

    # Save the tokenizer produced by the trainer temporarily.
    with tempfile.NamedTemporaryFile(
        suffix=".json",
        delete=False,
    ) as tmp:
        temp_tokenizer_file = tmp.name

    tokenizer.save(temp_tokenizer_file)

    with open(
        temp_tokenizer_file,
        "r",
        encoding="utf-8",
    ) as f:
        tokenizer_json = json.load(f)

    # Force the exact requested ID layout.
    tokenizer_json = remap_vocab(tokenizer_json)

    # Save final tokenizer.
    with open(
        TOKENIZER_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            tokenizer_json,
            f,
            ensure_ascii=False,
            indent=2,
        )

    # Reload the final tokenizer so evaluation tests the
    # actual tokenizer.json that will be used later.
    final_tokenizer = Tokenizer.from_file(
        TOKENIZER_FILE
    )

    # Configuration file.
    config = {
        "tokenizer_type": "byte_level_bpe",
        "vocab_size": 8192,

        "byte_vocab": {
            "start_id": 0,
            "end_id": 255,
            "size": 256,
        },

        "special_tokens": {
            "unk_token": "[-UNK-]",
            "unk_token_id": 256,

            "bos_token": "[-BOS-]",
            "bos_token_id": 257,

            "eos_token": "[-EOS-]",
            "eos_token_id": 258,
        },

        "learned_tokens": {
            "start_id": 259,
            "end_id": 8191,
            "size": 7933,
        },

        "pre_tokenizer": "ByteLevel",
        "decoder": "ByteLevel",

        "training": {
            "input_file": INPUT_FILE,
            "train_ratio": TRAIN_RATIO,
            "min_frequency": 2,
        },
    }

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            config,
            f,
            ensure_ascii=False,
            indent=2,
        )

    # Evaluate the final tokenizer.
    evaluate(
        final_tokenizer,
        eval_file,
    )

    # Final structural checks.
    vocab = final_tokenizer.get_vocab()

    assert len(vocab) == 8192

    assert final_tokenizer.token_to_id("[-UNK-]") == 256
    assert final_tokenizer.token_to_id("[-BOS-]") == 257
    assert final_tokenizer.token_to_id("[-EOS-]") == 258

    for i in range(256):
        assert final_tokenizer.id_to_token(i) is not None

    print()
    print("FINAL CHECKS")
    print("=" * 60)
    print("Vocabulary size : 8192")
    print("Byte IDs        : 0..255")
    print("UNK ID          : 256")
    print("BOS ID          : 257")
    print("EOS ID          : 258")
    print("Learned IDs     : 259..8191")
    print()
    print(f"Created: {TOKENIZER_FILE}")
    print(f"Created: {CONFIG_FILE}")
    print()
    print("Tokenizer training completed successfully.")


if __name__ == "__main__":
    main()
