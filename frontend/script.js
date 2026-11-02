// Frontend logic: strength metrics + calls to the Python backend.
// Owner: PhantomTDM (update)

const input = document.getElementById("password");
const bar = document.getElementById("meter-bar");
const rating = document.getElementById("rating");

function check(ok) { return ok ? "✓" : "✗"; }

function analyze(pw) {
  const lower = /[a-z]/.test(pw);
  const upper = /[A-Z]/.test(pw);
  const digit = /[0-9]/.test(pw);
  const symbol = /[^a-zA-Z0-9]/.test(pw);

  // Entropy estimate: length * log2(size of character pool)
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

  let label = "Very weak", color = "#d64545";
  if (m.entropy >= 80) { label = "Very strong"; color = "#1f9d55"; }
  else if (m.entropy >= 60) { label = "Strong"; color = "#5bb35b"; }
  else if (m.entropy >= 40) { label = "Fair"; color = "#e6a700"; }
  else if (m.entropy >= 28) { label = "Weak"; color = "#e57a2e"; }

  bar.style.width = Math.min(100, (m.entropy / 100) * 100) + "%";
  bar.style.background = color;
  rating.textContent = "Strength: " + (m.length ? label : "–");
}

input.addEventListener("input", update);

document.getElementById("generate").addEventListener("click", async () => {
  const res = await fetch("/api/generate?length=16");
  const data = await res.json();
  input.value = data.password;
  update();
});

document.getElementById("hash").addEventListener("click", async () => {
  if (!input.value) return;
  const res = await fetch("/api/hash", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: input.value }),
  });
  const data = await res.json();
  document.getElementById("sha-salt").textContent = data.sha256.salt;
  document.getElementById("sha-hash").textContent = data.sha256.hash;
  document.getElementById("bc-hash").textContent = data.bcrypt.hash;
  document.getElementById("results").hidden = false;
});
