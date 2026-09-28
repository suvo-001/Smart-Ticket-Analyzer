// ==========================================
// SmartTicket
// Frontend JavaScript
// ==========================================


// ===============================
// HTML Elements
// ===============================

const ticketInput =
    document.getElementById("ticket");

const charCount =
    document.getElementById("charCount");

const analyzeBtn =
    document.getElementById("analyzeBtn");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const emptyState =
    document.getElementById("emptyState");

const errorMessage =
    document.getElementById("errorMessage");


const category =
    document.getElementById("category");

const team =
    document.getElementById("team");

const priority =
    document.getElementById("priority");

const sentiment =
    document.getElementById("sentiment");

const confidence =
    document.getElementById("confidence");


// ===============================
// Character Counter
// ===============================

ticketInput.addEventListener("input", () => {

    const length =
        ticketInput.value.length;

    charCount.textContent =
        `${length} / 500`;

});


// ===============================
// Analyze Ticket
// ===============================

analyzeBtn.addEventListener(
    "click",
    async () => {

        const ticket =
            ticketInput.value.trim();


        // Empty ticket

        if (!ticket) {

            showError(
                "Please enter a support ticket."
            );

            return;

        }


        // Hide previous messages

        hideError();

        result.classList.add("hidden");


        // Show loading

        loading.classList.remove("hidden");

        analyzeBtn.disabled = true;


        try {

            // Send ticket to Flask API

            const response =
                await fetch(
                    "/analyze",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            ticket: ticket
                        })
                    }
                );


            const data =
                await response.json();


            // API error

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Unable to analyze ticket."
                );

            }


            // ===============================
            // Display Results
            // ===============================

            category.textContent =
                data.category || "Unknown";


            team.textContent =
                data.support_team ||
                "General Support";


            priority.textContent =
                data.priority ||
                "Low";


            sentiment.textContent =
                data.sentiment ||
                "Neutral";


            if (
                data.confidence !== undefined
            ) {

                confidence.textContent =
                    `${data.confidence}%`;

            } else {

                confidence.textContent =
                    "—";

            }


            // Hide empty state

            emptyState.classList.add("hidden");


            // Show results

            result.classList.remove("hidden");


        } catch (error) {

            console.error(
                "SmartTicket Error:",
                error
            );

            showError(
                error.message
            );

        } finally {

            loading.classList.add("hidden");

            analyzeBtn.disabled = false;

        }

    }
);


// ===============================
// Error Functions
// ===============================

function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove(
        "hidden"
    );

}


function hideError() {

    errorMessage.classList.add(
        "hidden"
    );

}