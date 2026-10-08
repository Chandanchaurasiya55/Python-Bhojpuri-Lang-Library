// BhojpuriPy Frontend Application Logic

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const sourceTextEl = document.getElementById("source-text");
  const targetTextEl = document.getElementById("target-text");
  const romanTextEl = document.getElementById("roman-text");
  const placeholderEl = document.getElementById("target-placeholder");
  const loadingEl = document.getElementById("loading-spinner");
  
  const sourceLangEl = document.getElementById("source-lang");
  const engineSelectEl = document.getElementById("engine-select");
  const dialectSelectEl = document.getElementById("dialect-select");
  const honorificSelectEl = document.getElementById("honorific-select");
  
  const charCountEl = document.getElementById("source-char-count");
  const latencyDisplayEl = document.getElementById("latency-display");
  const detectedPillEl = document.getElementById("detected-pill");
  
  const translateTriggerBtn = document.getElementById("translate-trigger-btn");
  const clearBtn = document.getElementById("clear-btn");
  const pasteBtn = document.getElementById("paste-btn");
  const copyBtn = document.getElementById("copy-btn");
  const speakBtn = document.getElementById("speak-btn");
  const viewToggleBtn = document.getElementById("view-toggle");
  const themeToggleBtn = document.getElementById("theme-toggle");
  
  const pythonCodeDisplayEl = document.getElementById("python-code-display");
  const copyCodeBtn = document.getElementById("copy-code-btn");
  
  const idiomBhojpuriEl = document.getElementById("idiom-bhojpuri");
  const idiomRomanEl = document.getElementById("idiom-roman");
  const idiomHindiEl = document.getElementById("idiom-hindi");
  const idiomEnglishEl = document.getElementById("idiom-english");
  const randomIdiomBtn = document.getElementById("random-idiom-btn");
  
  const toastEl = document.getElementById("toast");

  // State
  let debounceTimer = null;
  let showRoman = true;
  let allIdioms = [];
  let currentIdiomIdx = 0;

  // Show Toast
  function showToast(message) {
    toastEl.textContent = message;
    toastEl.classList.add("show");
    setTimeout(() => {
      toastEl.classList.remove("show");
    }, 2500);
  }

  // Update Character Count
  sourceTextEl.addEventListener("input", () => {
    const text = sourceTextEl.value;
    charCountEl.textContent = `${text.length} characters`;
    
    // Auto translate with debounce
    clearTimeout(debounceTimer);
    if (!text.trim()) {
      resetTarget();
      updatePythonCode();
      return;
    }
    
    debounceTimer = setTimeout(() => {
      performTranslation();
    }, 450);

    updatePythonCode();
  });

  // Reset Target
  function resetTarget() {
    placeholderEl.style.display = "flex";
    targetTextEl.style.display = "none";
    romanTextEl.style.display = "none";
    loadingEl.style.display = "none";
    detectedPillEl.style.display = "none";
    latencyDisplayEl.textContent = "⚡ Ready";
  }

  // Perform Translation
  async function performTranslation() {
    const text = sourceTextEl.value.trim();
    if (!text) {
      resetTarget();
      return;
    }

    // Show loading
    placeholderEl.style.display = "none";
    targetTextEl.style.display = "none";
    romanTextEl.style.display = "none";
    loadingEl.style.display = "flex";
    latencyDisplayEl.textContent = "⏳ Processing...";

    try {
      const payload = {
        text: text,
        source_lang: sourceLangEl.value,
        engine: engineSelectEl.value,
        dialect: dialectSelectEl.value,
        honorific: honorificSelectEl.value,
        include_roman: true
      };

      const res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();

      // Update UI
      loadingEl.style.display = "none";
      targetTextEl.textContent = data.bhojpuri;
      targetTextEl.style.display = "block";

      if (data.roman && showRoman) {
        romanTextEl.textContent = `🔤 ${data.roman}`;
        romanTextEl.style.display = "block";
      } else {
        romanTextEl.style.display = "none";
      }

      latencyDisplayEl.textContent = `⚡ ${data.execution_time_ms} ms (${data.engine})`;

      if (data.detected_lang && data.detected_lang !== "auto") {
        detectedPillEl.textContent = `Detected: ${data.detected_lang.toUpperCase()}`;
        detectedPillEl.style.display = "inline-block";
      } else {
        detectedPillEl.style.display = "none";
      }

      updatePythonCode(data.bhojpuri, data.roman);

    } catch (err) {
      loadingEl.style.display = "none";
      targetTextEl.textContent = "अनुवाद में कुछ समस्या भइल (Translation failed). Please try again.";
      targetTextEl.style.display = "block";
      latencyDisplayEl.textContent = "❌ Error";
    }
  }

  // Update Dynamic Python Code Display
  function updatePythonCode(bhojpuriOutput = "प्रणाम, रउआ कइसे बानी?", romanOutput = "Pranaam, rauaa kaise baanee?") {
    const textVal = sourceTextEl.value.trim() || "Hello, how are you?";
    const escapedText = textVal.replace(/"/g, '\\"');
    const dialectVal = dialectSelectEl.value;
    const engineVal = engineSelectEl.value;

    const codeSnippet = 
`import bhojpuripy as bho

# Translate to Bhojpuri
result = bho.translate(
    "${escapedText}",
    engine="${engineVal}",
    dialect="${dialectVal}"
)

print(result["bhojpuri"])  # ${bhojpuriOutput}
print(result["roman"])     # ${romanOutput}`;

    pythonCodeDisplayEl.textContent = codeSnippet;
  }

  // Event Listeners for Filters
  translateTriggerBtn.addEventListener("click", performTranslation);
  engineSelectEl.addEventListener("change", performTranslation);
  dialectSelectEl.addEventListener("change", performTranslation);
  honorificSelectEl.addEventListener("change", performTranslation);
  sourceLangEl.addEventListener("change", performTranslation);

  // Clear Button
  clearBtn.addEventListener("click", () => {
    sourceTextEl.value = "";
    charCountEl.textContent = "0 characters";
    resetTarget();
    updatePythonCode();
    sourceTextEl.focus();
  });

  // Paste Button
  pasteBtn.addEventListener("click", async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        sourceTextEl.value = text;
        sourceTextEl.dispatchEvent(new Event("input"));
      }
    } catch (e) {
      showToast("Clipboard access denied. Please paste manually.");
    }
  });

  // Copy Translation
  copyBtn.addEventListener("click", () => {
    const text = targetTextEl.textContent;
    if (text) {
      navigator.clipboard.writeText(text);
      showToast("Bhojpuri translation copied!");
    }
  });

  // Copy Python Code
  copyCodeBtn.addEventListener("click", () => {
    const code = pythonCodeDisplayEl.textContent;
    navigator.clipboard.writeText(code);
    showToast("Python code snippet copied!");
  });

  // Toggle Roman View
  viewToggleBtn.addEventListener("click", () => {
    showRoman = !showRoman;
    if (showRoman) {
      viewToggleBtn.classList.add("active");
      if (romanTextEl.textContent.trim()) {
        romanTextEl.style.display = "block";
      }
    } else {
      viewToggleBtn.classList.remove("active");
      romanTextEl.style.display = "none";
    }
  });

  // Audio Speech Synthesis (TTS)
  speakBtn.addEventListener("click", () => {
    const text = targetTextEl.textContent;
    if (!text || !('speechSynthesis' in window)) {
      showToast("Audio voice not supported in this browser.");
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "hi-IN"; // Indic/Hindi phonetics works closest for Bhojpuri Devanagari
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
    showToast("Playing pronunciation...");
  });

  // Quick Chips Click
  document.querySelectorAll(".phrase-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const phrase = chip.getAttribute("data-text");
      sourceTextEl.value = phrase;
      sourceTextEl.dispatchEvent(new Event("input"));
    });
  });

  // Theme Toggle
  themeToggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    const isDark = document.body.classList.contains("dark-theme");
    themeToggleBtn.querySelector(".theme-icon").textContent = isDark ? "☀️" : "🌙";
  });

  // Load Bhojpuri Idioms
  async function loadIdioms() {
    try {
      const res = await fetch("/api/idioms");
      if (res.ok) {
        const data = await res.json();
        allIdioms = data.idioms || [];
        if (allIdioms.length > 0) {
          displayIdiom(0);
        }
      }
    } catch (e) {
      console.log("Could not load idioms:", e);
    }
  }

  function displayIdiom(idx) {
    if (!allIdioms || allIdioms.length === 0) return;
    const item = allIdioms[idx % allIdioms.length];
    idiomBhojpuriEl.textContent = item.bhojpuri;
    idiomRomanEl.textContent = item.roman;
    idiomHindiEl.textContent = item.hindi;
    idiomEnglishEl.textContent = item.english;
  }

  randomIdiomBtn.addEventListener("click", () => {
    if (allIdioms.length > 0) {
      currentIdiomIdx = (currentIdiomIdx + 1) % allIdioms.length;
      displayIdiom(currentIdiomIdx);
    }
  });

  // Initial loads
  loadIdioms();
  updatePythonCode();
});
