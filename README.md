# Backend – Wirtualne Muzeum

## ✅ Jak uruchomić

### 1. Wymagania

- Docker + Docker Compose
- Konto na [ngrok.com](https://ngrok.com) + zainstalowany ngrok

---

### 2. Uruchomienie Dockera

```bash
docker compose up --build
```

Sprawdź, czy backend działa lokalnie na `http://localhost:8000/docs`

---

### 3. Uruchomienie Ngrok (tunnel do internetu)

```bash
ngrok config add-authtoken TWÓJ_TOKEN_TUTAJ  # tylko 1 raz!
ngrok http 8000
```

Ngrok poda Ci publiczny adres np.:

```
https://abcd-1234-xyz.ngrok-free.app
```

Ten adres trzeba wkleić do Vercel (w frontendzie) jako:

```
VITE_BACKEND_URL=https://abcd-1234-xyz.ngrok-free.app
```

Gotowe 🎉