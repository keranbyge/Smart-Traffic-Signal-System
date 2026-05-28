async function startSimulation() {

    let roads = [
        {
            name: "A",
            vehicles: parseInt(document.getElementById("inputA").value) || 0
        },

        {
            name: "B",
            vehicles: parseInt(document.getElementById("inputB").value) || 0
        },

        {
            name: "C",
            vehicles: parseInt(document.getElementById("inputC").value) || 0
        },

        {
            name: "D",
            vehicles: parseInt(document.getElementById("inputD").value) || 0
        }
    ];

    // Greedy Algorithm
    roads.sort((a, b) => b.vehicles - a.vehicles);

    for (let road of roads) {

        resetSignals();

        let signal = document.getElementById("signal" + road.name);

        signal.classList.remove("red");
        signal.classList.add("green");

        document.getElementById("current").innerHTML =
            `🟢 Road ${road.name} has highest traffic (${road.vehicles} vehicles)`;

        let greenTime = 2000;

        await sleep(greenTime);
    }

    resetSignals();

    document.getElementById("current").innerHTML =
        "✅ Traffic Simulation Completed";
}

function resetSignals() {

    let signals = document.querySelectorAll(".signal");

    signals.forEach(signal => {

        signal.classList.remove("green");
        signal.classList.add("red");

    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}