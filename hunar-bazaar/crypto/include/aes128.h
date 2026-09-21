#pragma once
#include <array>
#include <cstdint>
#include <string>
#include <vector>

namespace hb {

// Minimal AES-128 (ECB-mode, single 16-byte block) implementation, used to
// encrypt the small JSON payload (order id, agent id, expiry) embedded in
// each delivery QR code. Multi-block messages are handled with PKCS#7
// padding + block chaining (CBC) in EncryptCBC/DecryptCBC below.
class Aes128 {
public:
    static constexpr size_t kBlockSize = 16;
    static constexpr size_t kKeySize = 16;

    explicit Aes128(const std::array<uint8_t, kKeySize>& key);

    // Single 16-byte block, in place.
    void EncryptBlock(std::array<uint8_t, kBlockSize>& block) const;
    void DecryptBlock(std::array<uint8_t, kBlockSize>& block) const;

    // Whole-message helpers: PKCS#7 pad + CBC-chain across blocks.
    // IV is generated randomly and prepended to the returned ciphertext.
    std::vector<uint8_t> EncryptCBC(const std::vector<uint8_t>& plaintext) const;
    std::vector<uint8_t> DecryptCBC(const std::vector<uint8_t>& ciphertext_with_iv) const;

private:
    static constexpr int kRounds = 10;
    std::vector<std::array<uint8_t, 4>> round_keys_; // 4 words per round, 11 rounds -> 44 words

    void ExpandKey(const std::array<uint8_t, kKeySize>& key);
};

// Hex helpers used by the CLI to move bytes in/out of text form.
std::string ToHex(const std::vector<uint8_t>& bytes);
std::vector<uint8_t> FromHex(const std::string& hex);

} // namespace hb
