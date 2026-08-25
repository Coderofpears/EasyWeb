const form = document.querySelector("#contact-form");
const statusLine = document.querySelector("#form-status");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button");
  const payload = {
    source: "signal-contact-example",
    ...Object.fromEntries(new FormData(form).entries()),
  };

  button.disabled = true;
  statusLine.className = "form-status";
  statusLine.textContent = "Sending your signal...";

  try {
    const response = await fetch("/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.message || "The server did not accept the submission.");
    statusLine.textContent = `Saved at ${result.timestamp}. Thanks for reaching out.`;
    form.reset();
  } catch (error) {
    statusLine.className = "form-status error";
    statusLine.textContent = error.message || "Something went wrong. Try again.";
  } finally {
    button.disabled = false;
  }
});
