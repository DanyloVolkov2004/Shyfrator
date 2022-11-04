ciphers = {
    "AES": {
        "key_length": 32,
        "type": "block",
        "block_size": 16,
        "header_byte": b"\xae"
    },
    "Blowfish": {
        "key_length": 24,
        "type": "block",
        "block_size": 8,
        "header_byte": b"\xbf"
    },
    "Camellia": {
        "key_length": 16,
        "type": "block",
        "block_size": 16,
        "header_byte": b"\xca"
    },
    "ChaCha20": {
        "key_length": 32,
        "type": "stream",
        "nonce_size": 16,
        "header_byte": b"\xcc"
    }
}
