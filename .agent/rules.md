# Coding Rules & Standards - mychat

## 🛠 Tech Stack
- **Language:** Python 3.10+
- **Package Manager:** `uv` (Tuyệt đối không dùng `pip` trực tiếp).
- **Layout:** `src` layout pattern.
- **Web UI:** Gradio.
- **LLM API:** OpenAI SDK.
- **Testing:** `pytest`.

## 🏗 Architecture & Design
- **Paradigm:** Object-Oriented Programming (OOP). Ưu tiên tính đóng gói và kế thừa khi cần thiết.
- **Modularity:** Chia nhỏ code thành các module: `cli`, `web`, `core`, `storage`.
- **Data Safety:** Sử dụng `dataclasses` để định nghĩa schemas cho cấu hình và dữ liệu session.
- **Type Hinting:** Bắt buộc sử dụng Python Type Hints cho tất cả các hàm và method.

## 📝 Naming & Conventions
- Tuân thủ PEP 8.
- Biến và hàm dùng `snake_case`.
- Class dùng `PascalCase`.
- Hằng số dùng `UPPER_SNAKE_CASE`.