# Functional Instructions

## 1. CLI Commands
- `mychat` hoặc `mychat cli`: Chạy giao diện chat trong terminal.
- `mychat web`: Khởi tạo ứng dụng Gradio trên trình duyệt.

## 2. Environment & Credentials
- Lấy `OPENAI_API_KEY` từ biến môi trường. 
- Agent phải kiểm tra và thông báo lỗi rõ ràng nếu thiếu key này.

## 3. Storage Logic (Data Persistence)
- Thư mục làm việc: `data/`.
- **Config:** `data/config.json`. Nếu chưa có, tự động tạo mặc định:
  `{"system": "You are a helpful assistant.", "last_session_id": null}`.
- **Sessions:** Lưu tại `data/sessions/chat-<uuid>.json`.
- **Loading:** Luôn load JSON vào `dataclass` tương ứng trước khi xử lý để đảm bảo type-safe và default values.

## 4. Workflow
- Trước khi thực hiện thay đổi, hãy phân tích cấu trúc module hiện tại.
- Khi thêm feature mới, phải đảm bảo tính testable bằng cách viết kèm file test trong thư mục `tests/`.