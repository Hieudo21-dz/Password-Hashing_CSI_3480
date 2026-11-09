// Frontend logic are strength metrics, entropy calculation, and API calls
// with Mock testing fallback
// This is just a mock test to see if it work, will write after backend done

const input = document.getElementById("password");
const bar = document.getElementById("meter-bar");
const ratingText = document.getElementById("ratingText");

function check(ok) { return ok ? "✓" : "✗"; }

function analyze(pw) {
  const lower = /[a-z]/.test(pw);
  const upper = /[A-Z]/.test(pw);
  const digit = /[0-9]/.test(pw);
  const symbol = /[^a-zA-Z0-9]/.test(pw);

  let pool = 0;
  if (lower) pool += 26;
  if (upper) pool += 26;
  if (digit) pool += 10;
  if (symbol) pool += 32;
  const entropy = pw.length && pool ? Math.round(pw.length * Math.log2(pool)) : 0;

  return { length: pw.length, lower, upper, digit, symbol, entropy };
}

function update() {
  const m = analyze(input.value);
  document.getElementById("m-length").textContent = m.length;
  document.getElementById("m-lower").textContent = check(m.lower);
  document.getElementById("m-upper").textContent = check(m.upper);
  document.getElementById("m-digit").textContent = check(m.digit);
  document.getElementById("m-symbol").textContent = check(m.symbol);
  document.getElementById("m-entropy").textContent = m.entropy;

  let label = "Very weak", color = "#ef4444";
  if (m.entropy >= 80) { label = "Very strong"; color = "#10b981"; }
  else if (m.entropy >= 60) { label = "Strong"; color = "#34d399"; }
  else if (m.entropy >= 40) { label = "Fair"; color = "#fbbf24"; }
  else if (m.entropy >= 28) { label = "Weak"; color = "#f97316"; }

  bar.style.width = Math.min(100, (m.entropy / 100) * 100) + "%";
  bar.style.background = color;
  ratingText.textContent = "Strength: " + (m.length ? label : "–");
}

input.addEventListener("input", update);

// Generate Button calls API, falls back to local Mock Generator if backend is absent
document.getElementById("generateBtn").addEventListener("click", async () => {
  try {
    const res = await fetch("/api/generate?length=16");
    if (!res.ok) throw new Error("Backend endpoint missing");
    const data = await res.json();
    input.value = data.password;
  } catch (err) {
    console.warn("Backend not ready. Running Mock Generator fallback.");
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
    let mockPw = "";
    for (let i = 0; i < 16; i++) {
      mockPw += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    input.value = mockPw;
  }
  update();
});

// Hash Button Calls API, falls back to local Mock Hashes if backend is absent
document.getElementById("hashBtn").addEventListener("click", async () => {
  if (!input.value) return;

  try {
    const res = await fetch("/api/hash", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: input.value }),
    });
    if (!res.ok) throw new Error("Backend endpoint missing");
    const data = await res.json();
    document.getElementById("sha-salt").textContent = data.sha256.salt;
    document.getElementById("sha-hash").textContent = data.sha256.hash;
    document.getElementById("bc-hash").textContent = data.bcrypt.hash;
  } catch (err) {
    console.warn("Backend not ready. Running Mock Hashing fallback.");
    // Simulate realistic hash strings for UI demonstration testing
    document.getElementById("sha-salt").textContent = "9a7f3c1d0b2e8a4f";
    document.getElementById("sha-hash").textContent = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
    document.getElementById("bc-hash").textContent = "$2b$12$eImiTXuWVxfM37uY4JANjOL.5FD11b02H6Bf.B7g.2N1Y7Z6K4e2O";
  }

  document.getElementById("resultsCard").hidden = false;
});