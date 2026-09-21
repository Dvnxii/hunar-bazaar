// CLI wrapper so the Python backend (app/services/qr_service.py) can shell
// out to this binary rather than re-implementing AES in Python.
//
//   qr_crypto encrypt <hex_key_16bytes> <plaintext>       -> hex ciphertext (IV || CBC blocks)
//   qr_crypto decrypt <hex_key_16bytes> <hex_ciphertext>  -> plaintext
#include <algorithm>
#include <array>
#include <iostream>
#include <string>
#include <vector>

#include "aes128.h"

namespace {

std::array<uint8_t, 16> KeyFromHex(const std::string& hex) {
    auto bytes = hb::FromHex(hex);
    if (bytes.size() != 16) throw std::runtime_error("AES-128 key must be exactly 16 bytes (32 hex chars)");
    std::array<uint8_t, 16> key{};
    std::copy_n(bytes.begin(), 16, key.begin());
    return key;
}

int RunEncrypt(const std::string& key_hex, const std::string& plaintext) {
    hb::Aes128 aes(KeyFromHex(key_hex));
    std::vector<uint8_t> pt(plaintext.begin(), plaintext.end());
    auto ct = aes.EncryptCBC(pt);
    std::cout << hb::ToHex(ct) << std::endl;
    return 0;
}

int RunDecrypt(const std::string& key_hex, const std::string& ciphertext_hex) {
    hb::Aes128 aes(KeyFromHex(key_hex));
    auto ct = hb::FromHex(ciphertext_hex);
    auto pt = aes.DecryptCBC(ct);
    std::cout.write(reinterpret_cast<const char*>(pt.data()), static_cast<std::streamsize>(pt.size()));
    std::cout << std::endl;
    return 0;
}

} // namespace

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "Usage: qr_crypto <encrypt|decrypt> <hex_key> <text>" << std::endl;
        return 1;
    }
    std::string mode = argv[1], key_hex = argv[2], text = argv[3];
    try {
        if (mode == "encrypt") return RunEncrypt(key_hex, text);
        if (mode == "decrypt") return RunDecrypt(key_hex, text);
        std::cerr << "Unknown mode: " << mode << " (expected encrypt|decrypt)" << std::endl;
        return 1;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
