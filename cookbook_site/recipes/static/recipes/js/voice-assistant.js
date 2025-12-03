document.addEventListener("DOMContentLoaded", () => {
  const voiceBtn = document.getElementById("voiceAssistantBtn");
  const voicePanel = document.getElementById("voiceAssistantPanel");
  const voiceStatus = document.getElementById("voiceStatus");
  const voiceResponse = document.getElementById("voiceResponse");

  if (!voiceBtn || !voicePanel) return;

  let recognition = null;
  let isListening = false;
  let synth = window.speechSynthesis;

  // Check for browser support
  if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window)) {
    voiceBtn.disabled = true;
    voiceBtn.title = "Voice recognition not supported in this browser";
    return;
  }

  // Initialize speech recognition
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  recognition.onstart = () => {
    isListening = true;
    voiceBtn.classList.add("listening");
    voiceStatus.textContent = "🎤 Listening... Ask about ingredients or recipe ingredients!";
    voiceStatus.className = "voice-status listening";
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    voiceStatus.textContent = `You asked: "${transcript}"`;
    voiceStatus.className = "voice-status processing";
    voiceResponse.innerHTML = "";

    // Send query to backend
    fetch("/api/voice-assistant/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: transcript }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          displayResponse(data, true);
          speakResponse(data.message);
        } else {
          displayResponse(data, false);
          speakResponse(data.message);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        voiceStatus.textContent = "Sorry, I encountered an error. Please try again.";
        voiceStatus.className = "voice-status error";
      });
  };

  recognition.onerror = (event) => {
    isListening = false;
    voiceBtn.classList.remove("listening");
    let errorMsg = "Sorry, I couldn't hear you. Please try again.";
    
    if (event.error === "no-speech") {
      errorMsg = "No speech detected. Please try again.";
    } else if (event.error === "not-allowed") {
      errorMsg = "Microphone access denied. Please enable it in your browser settings.";
    }
    
    voiceStatus.textContent = errorMsg;
    voiceStatus.className = "voice-status error";
  };

  recognition.onend = () => {
    isListening = false;
    voiceBtn.classList.remove("listening");
    if (!voiceStatus.textContent.includes("You asked") && !voiceStatus.textContent.includes("Sorry")) {
      voiceStatus.textContent = "Click the microphone to ask about ingredients or recipe ingredients";
      voiceStatus.className = "voice-status";
    }
  };

  voiceBtn.addEventListener("click", () => {
    if (isListening) {
      recognition.stop();
    } else {
      voicePanel.style.display = "block";
      recognition.start();
    }
  });

  function displayResponse(data, success) {
    if (success) {
      if (data.type === "recipe_ingredients") {
        // Display recipe ingredients
        voiceStatus.textContent = `Ingredients for ${data.recipe}:`;
        voiceStatus.className = "voice-status success";
        
        const ingredientsList = data.ingredients.map(ing => `<li>${ing}</li>`).join("");
        voiceResponse.innerHTML = `
          <div class="recipe-ingredients-info">
            <h3>${data.recipe}</h3>
            <p class="recipe-link"><a href="/recipes/${data.recipe_slug}/">View full recipe →</a></p>
            <h4>Ingredients:</h4>
            <ul class="recipe-ingredients-list">
              ${ingredientsList}
            </ul>
          </div>
        `;
      } else if (data.type === "ingredient_info") {
        // Display ingredient information
        voiceStatus.textContent = `Information about ${data.ingredient}:`;
        voiceStatus.className = "voice-status success";
        
        voiceResponse.innerHTML = `
          <div class="ingredient-info">
            <h3>${data.ingredient}</h3>
            <p><strong>Description:</strong> ${data.description}</p>
            <p><strong>Storage:</strong> ${data.storage}</p>
            <p><strong>Uses:</strong> ${data.uses}</p>
          </div>
        `;
      }
    } else {
      voiceStatus.textContent = data.message;
      voiceStatus.className = "voice-status error";
      voiceResponse.innerHTML = "";
    }
  }

  function speakResponse(text) {
    if (synth && synth.speaking) {
      synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 0.8;
    synth.speak(utterance);
  }

  // Helper function to get CSRF token
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

