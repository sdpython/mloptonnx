#include <vector>
#include <sstream>

template <typename T>
inline void MakeStringInternal(std::ostringstream& ss, const T& t) noexcept {
    ss << t;
}

template <>
inline void MakeStringInternal(std::ostringstream& ss, const std::vector<int32_t>& t) noexcept {
    for(auto it: t)
        ss << "x" << it;
}

template <>
inline void MakeStringInternal(std::ostringstream& ss, const std::vector<uint32_t>& t) noexcept {
    for(auto it: t)
        ss << "x" << it;
}

template <>
inline void MakeStringInternal(std::ostringstream& ss, const std::vector<int64_t>& t) noexcept {
    for(auto it: t)
        ss << "x" << it;
}

template <>
inline void MakeStringInternal(std::ostringstream& ss, const std::vector<uint64_t>& t) noexcept {
    for(auto it: t)
        ss << "x" << it;
}

template <>
inline void MakeStringInternal(std::ostringstream& ss, const std::vector<int16_t>& t) noexcept {
    for(auto it: t)
        ss << "x" << it;
}

template <>
inline void MakeStringInternal(std::ostringstream& ss, const std::vector<uint16_t>& t) noexcept {
    for(auto it: t)
        ss << "x" << it;
}

template <typename T, typename... Args>
inline void MakeStringInternal(std::ostringstream& ss, const T& t, const Args&... args) noexcept {
    MakeStringInternal(ss, t);
    MakeStringInternal(ss, args...);
}

template <typename... Args>
inline std::string MakeString(const Args&... args) {
    std::ostringstream ss;
    MakeStringInternal(ss, args...);
    return std::string(ss.str());
}
