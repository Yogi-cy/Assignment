
- Notice there are **three backticks**, `mermaid` immediately after the first backticks, and then your Mermaid code.  
- Save the file as `.md` and view it on GitHub. It will render as a **proper flowchart**, not plain text.

---

### **2️⃣ Optional: Use a GitHub extension or editor**
- If you preview locally, some editors like **VS Code with “Markdown Preview Mermaid Support”** render it live.  
- On GitHub, the above fenced block works out-of-the-box.

---

### **3️⃣ Example with your flowchart**
Here’s how your **sequential + inline description flowchart** should appear in your README:

```markdown
```mermaid
flowchart TD

    A[Step 1️⃣ Start Process] --> B[Step 2️⃣ logStartingOfProcessToMongo<br/><sub>Insert process start record into Mongo</sub>]

    B --> C{Step 3️⃣ For Each Country<br/><sub>Loop over processingCountries</sub>}

    C --> C1[Step 3.1 Load Coordinates<br/><sub>Get polygon/chunks for country</sub>]
    C1 --> C2[Step 3.2 generateInsideCountryDevicesQuery<br/><sub>Find devices inside country in last X hours</sub>]
    C2 --> C3[Step 3.3 Filter Device IDs<br/><sub>Keep only valid unique devices</sub>]
    C3 --> C4[Step 3.4 generateOutsideCountryDevicesQuery<br/><sub>Check if those devices appeared outside country</sub>]
    C4 --> C5[Step 3.5 updateForeignTravelDevices<br/><sub>Insert/Update devices per country in Mongo</sub>]
    C5 --> C6[Step 3.6 updateCountryProcessStatus<br/><sub>Mark country status (success/failure)</sub>]

    C6 --> D{Step 4️⃣ More Countries?<br/><sub>Any left to process?</sub>}
    D -- Yes --> C1
    D -- No --> E[Step 5️⃣ finalizeProcessStatus<br/><sub>Evaluate process outcome</sub>]

    E --> F{Step 6️⃣ Evaluate Final Status<br/><sub>Look at all processedCountries</sub>}
    F -- All Success --> G[Step 6.1 Completed<br/><sub>Status = completed</sub>]
    F -- All Failure --> H[Step 6.2 Failed<br/><sub>Status = failed</sub>]
    F -- Partial --> I[Step 6.3 Partial<br/><sub>Status = partial</sub>]

    G --> J[Step 7️⃣ Update process document<br/><sub>Set endTime + resultDocId</sub>]
    H --> J
    I --> J

    J --> K[Step 8️⃣ End Process<br/><sub>Pipeline finished</sub>]
