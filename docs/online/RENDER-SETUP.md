# Free public SmartServe demo

1. Create a free Neon PostgreSQL project and copy its connection string.
2. In Render, choose **New → Blueprint** and select this repository.
3. Select the branch containing this file and the root `render.yaml`.
4. Leave Blueprint Path empty, or enter `render.yaml`.
5. Paste the Neon connection string into Render's `DATABASE_URL` field.
6. Keep the Free service plan and deploy.
7. Open the service's public URL, check `/health`, and check the menu and owner dashboard.

The React frontend and FastAPI API share one origin. Local Vite development
continues to use `http://localhost:8000` by default. `VITE_API_URL` can override
that choice at frontend build time.

The new Neon database starts with demo data. This does not copy local stock,
orders, or sales. Use only sample data: payments are simulated, and the current
repository version does not enforce owner authentication. Visitors share the
same demo database and can change its data.

Render's free service sleeps after 15 idle minutes and wakes when visited.
The first visit can be slow. Both services have free usage limits. Store the
database URL only in Render environment settings, never in the repository.
