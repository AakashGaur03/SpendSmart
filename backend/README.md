# Backend (Express + TypeScript)

Node/Express API that sits between the frontend and the ML service. Uses MongoDB for expenses.

## Setup

1. Copy environment file and set variables:

   ```bash
   cp .env.example .env
   ```

   Edit `.env`: set `MONGO_URI` (e.g. `mongodb://localhost:27017/spendsmart`) and optionally `ML_SERVICE_URL` (default `http://localhost:8000`).

2. Install dependencies and run:
   ```bash
   npm install
   npm run dev
   ```
   Server runs on `http://localhost:4000`.

## Prerequisites

- **MongoDB** running locally or a connection string.
- **ML service** running at `ML_SERVICE_URL` (default `http://localhost:8000`) for predictions and feedback. If the ML service is down, new expenses still save with category "Other".

## API

- `GET /api/health` – health check
- `GET /api/expenses` – list expenses (newest first)
- `POST /api/expenses` – create expense (body: `{ description, amount?, date? }`). Calls ML service to predict category.
- `PATCH /api/expenses/:id` – update expense (body: `{ category }`). Sends feedback to ML if category was corrected.
- `DELETE /api/expenses/:id` – delete expense
