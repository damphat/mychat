# Project Context: mychat

## Overview
`mychat` là một công cụ CLI giúp tương tác với OpenAI API một cách linh hoạt qua cả Terminal và Web (Gradio). Dự án tập trung vào tính gọn nhẹ, quản lý session thông minh và dễ mở rộng.

## Expected Directory Structure
```text
mychat/
├── .agent/
│   ├── rules.md
│   ├── instructions.md
│   └── project-context.md
├── data/
│   ├── config.json
│   └── sessions/
├── src/
│   └── mychat/
│       ├── __init__.py
│       ├── main.py
│       ├── core/       # Logic gọi API, quản lý hội thoại
│       ├── storage/    # Xử lý dataclasses, đọc/ghi JSON
│       └── ui/         # CLI và Gradio interface
├── tests/
├── pyproject.toml      # Quản lý bởi uv
└── .env