# Frontend (React + TypeScript)

Vite + React app for adding and managing expenses with ML-powered category suggestions.

## Setup

```bash
npm install
npm run dev
```

Runs on `http://localhost:5173`. API requests are proxied to the backend at `http://localhost:4000` (see `vite.config.ts`).

## Prerequisites

- **Backend** running on port 4000.
- **ML service** running (backend uses it for predictions).

## Features

- Add expense with description (and optional amount); category is predicted by the ML service.
- View list of expenses with predicted category and confidence (high/medium/low).
- Edit category; corrections are sent to the ML service as feedback for future retraining.
- Delete expenses.
