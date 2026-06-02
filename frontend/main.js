const API_BASE = "http://localhost:8000";

function getToken() {
  return localStorage.getItem("access_token") || "";
}

function setToken(token) {
  if (token) localStorage.setItem("access_token", token);
  else localStorage.removeItem("access_token");
}

function pretty(obj) {
  return JSON.stringify(obj, null, 2);
}

async function api(path, options = {}) {
  const token = getToken();
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
    ...options,
  });
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { raw: text };
  }
  if (!res.ok) throw { status: res.status, data };
  return data;
}

const el = (id) => document.getElementById(id);

function setDefaultGql() {
  el("gqlQuery").value = `query($vin: String!) {
  maintenanceHistory(vin: $vin) {
    currentKm
    car { vin make model }
    plans {
      serviceType intervalKm lastDoneKm nextDueKm currentKm remainingKm dueSoon overdue
    }
    records {
      serviceType date odometerKm cost notes
    }
  }
}`;
}

setDefaultGql();

// Auth
el("btnRegister").addEventListener("click", async () => {
  try {
    const payload = {
      username: el("authUsername").value.trim(),
      email: el("authEmail").value.trim(),
      password: el("authPassword").value,
    };
    const data = await api("/api/auth/register/", { method: "POST", body: JSON.stringify(payload) });
    el("authOut").textContent = pretty(data);
  } catch (e) {
    el("authOut").textContent = pretty(e);
  }
});

el("btnLogin").addEventListener("click", async () => {
  try {
    const payload = {
      username: el("authUsername").value.trim(),
      password: el("authPassword").value,
    };
    const data = await api("/api/auth/token/", { method: "POST", body: JSON.stringify(payload) });
    setToken(data.access);
    el("authOut").textContent = pretty({ ok: true, token_saved: true, ...data });
  } catch (e) {
    el("authOut").textContent = pretty(e);
  }
});

el("btnMe").addEventListener("click", async () => {
  try {
    const data = await api("/api/auth/me/");
    el("authOut").textContent = pretty(data);
  } catch (e) {
    el("authOut").textContent = pretty(e);
  }
});

el("btnLogout").addEventListener("click", () => {
  setToken("");
  el("authOut").textContent = pretty({ ok: true, logged_out: true });
});

el("btnForgot").addEventListener("click", async () => {
  try {
    const payload = { email: el("forgotEmail").value.trim() };
    const data = await api("/api/auth/password/forgot/", { method: "POST", body: JSON.stringify(payload) });
    el("authOut").textContent = pretty(data);
  } catch (e) {
    el("authOut").textContent = pretty(e);
  }
});

el("btnResetConfirm").addEventListener("click", async () => {
  try {
    const payload = {
      uid: el("resetUid").value.trim(),
      token: el("resetToken").value.trim(),
      new_password: el("resetNewPassword").value,
    };
    const data = await api("/api/auth/password/reset/", { method: "POST", body: JSON.stringify(payload) });
    el("authOut").textContent = pretty(data);
  } catch (e) {
    el("authOut").textContent = pretty(e);
  }
});

// REST: spare part orders
el("btnCreateOrder").addEventListener("click", async () => {
  try {
    const payload = {
      car: Number(el("orderCarId").value),
      part_name: el("orderPartName").value.trim(),
      part_number: el("orderPartNumber").value.trim(),
      quantity: Number(el("orderQty").value || "1"),
      status: el("orderStatus").value.trim() || "draft",
      vendor: el("orderVendor").value.trim(),
      price: el("orderPrice").value.trim() || null,
      ordered_at: el("orderOrderedAt").value.trim() || null,
      notes: el("orderNotes").value.trim(),
    };
    const data = await api("/api/spare-part-orders/", { method: "POST", body: JSON.stringify(payload) });
    el("ordersOut").textContent = pretty(data);
  } catch (e) {
    el("ordersOut").textContent = pretty(e);
  }
});

el("btnListOrders").addEventListener("click", async () => {
  try {
    const data = await api("/api/spare-part-orders/");
    el("ordersOut").textContent = pretty(data);
  } catch (e) {
    el("ordersOut").textContent = pretty(e);
  }
});

// REST: cars
el("btnCreateCar").addEventListener("click", async () => {
  try {
    const payload = {
      vin: el("carVin").value.trim(),
      make: el("carMake").value.trim(),
      model: el("carModel").value.trim(),
    };
    const data = await api("/api/cars/", { method: "POST", body: JSON.stringify(payload) });
    el("restCarsOut").textContent = pretty(data);
  } catch (e) {
    el("restCarsOut").textContent = pretty(e);
  }
});

el("btnListCars").addEventListener("click", async () => {
  try {
    const data = await api("/api/cars/");
    el("restCarsOut").textContent = pretty(data);
  } catch (e) {
    el("restCarsOut").textContent = pretty(e);
  }
});

// REST: fillups
el("btnCreateFill").addEventListener("click", async () => {
  try {
    const payload = {
      car: Number(el("fillCarId").value),
      date: el("fillDate").value.trim(),
      odometer_km: Number(el("fillKm").value),
      liters: el("fillLiters").value,
      total_cost: el("fillCost").value,
    };
    const data = await api("/api/fuel-fillups/", { method: "POST", body: JSON.stringify(payload) });
    el("restFillOut").textContent = pretty(data);
  } catch (e) {
    el("restFillOut").textContent = pretty(e);
  }
});

el("btnListFill").addEventListener("click", async () => {
  try {
    const data = await api("/api/fuel-fillups/");
    el("restFillOut").textContent = pretty(data);
  } catch (e) {
    el("restFillOut").textContent = pretty(e);
  }
});

// GraphQL
el("btnRunGql").addEventListener("click", async () => {
  try {
    const vin = el("gqlVin").value.trim();
    const query = el("gqlQuery").value;
    const data = await api("/graphql/", {
      method: "POST",
      body: JSON.stringify({ query, variables: { vin } }),
    });
    el("gqlOut").textContent = pretty(data);
  } catch (e) {
    el("gqlOut").textContent = pretty(e);
  }
});

el("btnResetGql").addEventListener("click", () => setDefaultGql());

// WebSocket
let ws = null;

function wsStatus(obj) {
  el("wsOut").textContent = pretty(obj);
}

el("btnWsConnect").addEventListener("click", () => {
  try {
    if (ws && ws.readyState === WebSocket.OPEN) return;
    const url = "ws://localhost:8000/ws/reminders/";
    ws = new WebSocket(url);
    wsStatus({ status: "connecting", url });
    ws.onopen = () => wsStatus({ status: "connected", url });
    ws.onmessage = (ev) => {
      try {
        wsStatus(JSON.parse(ev.data));
      } catch {
        wsStatus({ type: "raw", data: ev.data });
      }
    };
    ws.onclose = () => wsStatus({ status: "disconnected" });
    ws.onerror = () => wsStatus({ status: "error" });
  } catch (e) {
    wsStatus({ status: "error", e });
  }
});

el("btnWsDisconnect").addEventListener("click", () => {
  if (ws) ws.close();
  ws = null;
  wsStatus({ status: "disconnected" });
});

