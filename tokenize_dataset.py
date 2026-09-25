"""
Streaming dataset preparation for 5555LM.

Input:
    fineweb_sample.txt

Tokenizer:
    tokenizers/tokenizer.json

Output:
    data/train.bin
    data/val.bin
    data/dataset_config.json

Features:
    - 90/10 train/validation split
    - Streaming input
    - Bounded RAM usage
    - UTF-8 safe
    - uint16 token IDs
    - Works with very large datasets
    - Does NOT load the entire dataset into RAM
"""

import json
from array import array
from pathlib import Path

from tokenizers import Tokenizer


# ============================================================
# CONFIG
# ============================================================

RAW_DATA = Path("fineweb_sample.txt")

TOKENIZER_FILE = Path("tokenizers/tokenizer.json")

OUTPUT_DIR = Path("data")

TRAIN_FILE = OUTPUT_DIR / "train.bin"
VAL_FILE = OUTPUT_DIR / "val.bin"

DATASET_CONFIG_FILE = OUTPUT_DIR / "dataset_config.json"

TRAIN_RATIO = 0.90

CHUNK_SIZE = 8 * 1024 * 1024

TOKEN_BUFFER_SIZE = 1_000_000


# ============================================================
# VALIDATION
# ============================================================

def validate_configuration(tokenizer):
    vocab_size = tokenizer.get_vocab_size()

    if vocab_size > 65536:
        raise ValueError(
            f"Vocabulary size is {vocab_size:,}, "
            "which cannot fit into uint16."
        )

    print(f"Vocabulary size : {vocab_size:,}")
    print("Token dtype     : uint16")
    print("Token range     : 0 - 65,535")


# ============================================================
# FIND 90/10 SPLIT
# ============================================================

def find_split_position():
    print()
    print("=" * 70)
    print("FINDING TRAIN / VALIDATION SPLIT")
    print("=" * 70)

    file_size = RAW_DATA.stat().st_size

    target_position = int(file_size * TRAIN_RATIO)

    print(f"Raw file size : {file_size:,} bytes")
    print(
        f"Target train  : "
        f"{target_position:,} bytes "
        f"({TRAIN_RATIO * 100:.1f}%)"
    )

    with open(RAW_DATA, "rb") as f:
        f.seek(target_position)
        f.readline()

        split_position = f.tell()

    train_bytes = split_position
    val_bytes = file_size - split_position

    print()
    print(
        f"Actual train  : {train_bytes:,} bytes "
        f"({train_bytes / file_size * 100:.2f}%)"
    )

    print(
        f"Actual val    : {val_bytes:,} bytes "
        f"({val_bytes / file_size * 100:.2f}%)"
    )

    return split_position


# ============================================================
# TOKEN BUFFER
# ============================================================

class TokenWriter:

    def __init__(self, path):
        self.path = path
        self.file = open(path, "wb")

        self.buffer = array("H")

        self.total_tokens = 0

    def add(self, token_ids):
        self.buffer.extend(token_ids)

        if len(self.buffer) >= TOKEN_BUFFER_SIZE:
            self.flush()

    def flush(self):
        if not self.buffer:
            return

        self.file.write(self.buffer.tobytes())

        self.total_tokens += len(self.buffer)

        self.buffer.clear()

    def close(self):
        self.flush()
        self.file.close()


# ============================================================
# STREAMING TOKENIZATION
# ============================================================

def tokenize_range(
    tokenizer,
    start,
    end,
    output_file,
    label,
):
    writer = TokenWriter(output_file)

    processed_bytes = 0

    leftover = b""

    with open(RAW_DATA, "rb") as src:

        src.seek(start)

        while start + processed_bytes < end:

            remaining = end - (start + processed_bytes)

            read_size = min(CHUNK_SIZE, remaining)

            data = src.read(read_size)

            if not data:
                break

            processed_bytes += len(data)

            if leftover:
                data = leftover + data
                leftover = b""

            try:
                text = data.decode("utf-8")

            except UnicodeDecodeError as error:

                valid_data = data[:error.start]

                leftover = data[error.start:]

                text = valid_data.decode("utf-8")

            if text:

                encoding = tokenizer.encode(text)

                writer.add(encoding.ids)

            if processed_bytes % (256 * 1024 * 1024) < CHUNK_SIZE:

                percentage = (
                    processed_bytes /
                    (end - start)
                ) * 100

                print(
                    f"\r{label}: "
                    f"{percentage:6.2f}% | "
                    f"{processed_bytes:,} bytes | "
                    f"{writer.total_tokens:,} tokens",
                    end="",
                    flush=True,
                )

    if leftover:

        text = leftover.decode("utf-8")

        if text:

            encoding = tokenizer.encode(text)

            writer.add(encoding.ids)

    writer.close()

    print()

    return writer.total_tokens


# ============================================================
# FILE SIZE HELPER
# ============================================================

def file_size_mb(path):
    return path.stat().st_size / (1024 * 1024)


# ============================================================
# MAIN
# ============================================================

def main():

    # ========================================================
    # CHECK INPUTS
    # ========================================================

    if not RAW_DATA.exists():
        raise FileNotFoundError(
            f"Raw dataset not found:\n"
            f"    {RAW_DATA.resolve()}"
        )

    if not TOKENIZER_FILE.exists():
        raise FileNotFoundError(
            f"Tokenizer not found:\n"
            f"    {TOKENIZER_FILE.resolve()}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # LOAD TOKENIZER
    # ========================================================

    print("=" * 70)
    print("5555LM STREAMING DATASET PREPARATION")
    print("=" * 70)

    print()
    print(f"Raw data       : {RAW_DATA}")
    print(f"Tokenizer      : {TOKENIZER_FILE}")
    print(f"Output dir     : {OUTPUT_DIR}")
    print(f"Train ratio    : {TRAIN_RATIO:.2f}")
    print(f"Val ratio      : {1.0 - TRAIN_RATIO:.2f}")
    print(
        f"Chunk size     : "
        f"{CHUNK_SIZE / 1024 / 1024:.1f} MiB"
    )
    print(
        f"Token buffer   : "
        f"{TOKEN_BUFFER_SIZE:,} tokens"
    )

    print()
    print("Loading tokenizer...")

    tokenizer = Tokenizer.from_file(
        str(TOKENIZER_FILE)
    )

    validate_configuration(tokenizer)

    vocab_size = tokenizer.get_vocab_size()

    # ========================================================
    # FIND SPLIT
    # ========================================================

    split_position = find_split_position()

    file_size = RAW_DATA.stat().st_size

    # ========================================================
    # TOKENIZE TRAIN
    # ========================================================

    print()
    print("=" * 70)
    print("TOKENIZING TRAIN")
    print("=" * 70)

    train_tokens = tokenize_range(
        tokenizer=tokenizer,
        start=0,
        end=split_position,
        output_file=TRAIN_FILE,
        label="Train",
    )

    # ========================================================
    # TOKENIZE VALIDATION
    # ========================================================

    print()
    print("=" * 70)
    print("TOKENIZING VALIDATION")
    print("=" * 70)

    val_tokens = tokenize_range(
        tokenizer=tokenizer,
        start=split_position,
        end=file_size,
        output_file=VAL_FILE,
        label="Val",
    )

    # ========================================================
    # DATASET CONFIG
    # ========================================================

    total_tokens = train_tokens + val_tokens

    actual_train_ratio = (
        train_tokens / total_tokens
        if total_tokens > 0
        else 0
    )

    actual_val_ratio = (
        val_tokens / total_tokens
        if total_tokens > 0
        else 0
    )

    config = {
        "raw_data": str(RAW_DATA),
        "tokenizer": str(TOKENIZER_FILE),

        "vocab_size": vocab_size,

        "token_dtype": "uint16",
        "token_bytes": 2,

        "requested_train_ratio": TRAIN_RATIO,
        "requested_val_ratio": 1.0 - TRAIN_RATIO,

        "actual_train_ratio": actual_train_ratio,
        "actual_val_ratio": actual_val_ratio,

        "raw_file_bytes": file_size,

        "train_raw_bytes": split_position,
        "val_raw_bytes": file_size - split_position,

        "train_tokens": train_tokens,
        "val_tokens": val_tokens,
        "total_tokens": total_tokens,

        "train_file": str(TRAIN_FILE),
        "val_file": str(VAL_FILE),
    }

    with open(
        DATASET_CONFIG_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            config,
            f,
            indent=2,
        )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 70)
    print("DATASET READY")
    print("=" * 70)

    print()
    print("RAW DATA")
    print("-" * 70)
    print(f"Size       : {file_size_mb(RAW_DATA):,.2f} MiB")
    print(f"Train raw  : {split_position:,} bytes")
    print(f"Val raw    : {file_size - split_position:,} bytes")

    print()
    print("TOKENS")
    print("-" * 70)
    print(f"Train      : {train_tokens:,}")
    print(f"Validation : {val_tokens:,}")
    print(f"Total      : {total_tokens:,}")

    print()
    print("TOKEN RATIO")
    print("-" * 70)
    print(f"Train      : {actual_train_ratio * 100:.2f}%")
    print(f"Validation : {actual_val_ratio * 100:.2f}%")

    print()
    print("OUTPUT FILES")
    print("-" * 70)
    print(
        f"Train      : {TRAIN_FILE} "
        f"({file_size_mb(TRAIN_FILE):,.2f} MiB)"
    )
    print(
        f"Validation : {VAL_FILE} "
        f"({file_size_mb(VAL_FILE):,.2f} MiB)"
    )
    print(f"Config     : {DATASET_CONFIG_FILE}")

    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
