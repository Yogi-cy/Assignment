flowchart TD

    A[Start Process] --> B[logStartingOfProcessToMongo]
    B --> C{For Each Country}

    C --> C1[Load Coordinates<br/>- country polygon<br/>- country chunks]
    C1 --> C2[Query inside devices<br/>generateInsideCountryDevicesQuery]
    C2 --> C3[Filter valid device IDs]
    C3 --> C4[Query outside devices<br/>generateOutsideCountryDevicesQuery]
    C4 --> C5[updateForeignTravelDevices<br/>(Insert/Update in Mongo)]
    C5 --> C6[updateCountryProcessStatus<br/>processedCountries.<country>]

    C6 --> D{More Countries?}
    D -- Yes --> C1
    D -- No --> E[finalizeProcessStatus]

    E --> F{Evaluate Final Status}
    F -- All Success --> G[Status = Completed]
    F -- All Failure --> H[Status = Failed]
    F -- Partial --> I[Status = Partial]

    G --> J[Update process document<br/>processingEndDateTime + resultDocId]
    H --> J
    I --> J

    J --> K[End Process]
