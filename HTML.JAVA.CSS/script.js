const form = document.getElementById("record-form");
const chainOutput = document.getElementById("chain-output");

const demoChain = [];

//helper to convert ArrayBuffer to hex string
function bufferToHex(buffer) {
    const bytes = new Uint8Array(buffer);
    return Array.from(bytes)
        .map(b => b.toString(16).padStart(2, "0"))
        .join("");
}

//use browser's Web Crypto API to hash with SHA-256
async function sha256(message) {
    const encoder = new TextEncoder();
    const data = encoder.encode(message);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    return bufferToHex(hashBuffer);
}

function renderChain() {
    if (demoChain.length === 0) {
        chainOutput.innerHTML = "<p>No blocks yet. Add a record above.</p>";
        return;
    }

    chainOutput.innerHTML = "";

    demoChain.forEach(block => {
        const blockDiv = document.createElement("div");
        blockDiv.className = "block";

        blockDiv.innerHTML = `
            <div class="block-header">
                <span>Block #${block.index}</span>
                <span>${new Date(block.timestamp).toLocaleTimeString()}</span>
            </div>
            <div class="block-data">
                <strong>Patient ID:</strong> ${block.patientId}<br>
                <strong>Record:</strong> ${block.record}
            </div>
            <div class="block-hash">
                <strong>Hash:</strong> ${block.hash}
            </div>
        `;

        const tamperButton = document.createElement("button");
        tamperButton.textContent = "Tamper";
        tamperButton.type = "button";

        tamperButton.onclick = async () => {
            const tamperedRecord = block.record + " [tampered]";
            const payload = JSON.stringify({
                patientId: block.patientId,
                recordData: tamperedRecord,
                previousHash: block.previousHash,
                timestamp: Date.now(),
            });
            const newHash = await sha256(payload);

            block.record = tamperedRecord;
            block.hash = newHash;
            block.timestamp = Date.now();

            renderChain();
        };

        blockDiv.appendChild(tamperButton);
        chainOutput.appendChild(blockDiv);
    });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const patientId = document.getElementById("patient-id").value.trim();
    const recordData = document.getElementById("record-data").value.trim();

    if (!patientId || !recordData) {
        return;
    }

    const previousHash =
        demoChain.length === 0 ? "0" : demoChain[demoChain.length - 1].hash;

    const payload = JSON.stringify({
        patientId,
        recordData,
        previousHash,
        timestamp: Date.now(),
    });

    const hash = await sha256(payload);

    const block = {
        index: demoChain.length,
        patientId,
        record: recordData,
        previousHash,
        timestamp: Date.now(),
        hash,
    };

    demoChain.push(block);
    renderChain();

    form.reset();
});
