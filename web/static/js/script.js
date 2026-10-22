document.addEventListener("DOMContentLoaded", function() {

    console.log("=================================");
    console.log("DIGITAL FOOTPRINT ANALYZER");
    console.log("JavaScript loaded successfully");
    console.log("=================================");


    // =========================================================
    // BASIC HELPERS
    // =========================================================

    const $ = function(id) {
        return document.getElementById(id);
    };


    function showToast(title, message) {

        const toast = $("toast");
        const toastTitle = $("toastTitle");
        const toastMessage = $("toastMessage");

        if (!toast) {
            alert(message);
            return;
        }

        toastTitle.textContent = title;
        toastMessage.textContent = message;

        toast.classList.add("show");

        setTimeout(function() {
            toast.classList.remove("show");
        }, 3500);
    }


    function setText(id, value) {

        const element = $(id);

        if (element) {
            element.textContent =
                value !== undefined &&
                value !== null ?
                value :
                "—";
        }
    }


    function escapeHTML(value) {

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    // =========================================================
    // NAVIGATION / SWITCHES
    // =========================================================

    const navButtons =
        document.querySelectorAll(".nav-btn");

    const toolSections =
        document.querySelectorAll(".tool-section");


    navButtons.forEach(function(button) {

        button.addEventListener("click", function() {

            const sectionId =
                button.getAttribute("data-section");

            navButtons.forEach(function(item) {
                item.classList.remove("active");
            });

            toolSections.forEach(function(section) {
                section.classList.remove("active-section");
            });

            button.classList.add("active");

            const target =
                $(sectionId);

            if (target) {

                target.classList.add("active-section");

                window.scrollTo({
                    top: target.offsetTop - 100,
                    behavior: "smooth"
                });
            }

        });

    });


    // =========================================================
    // BACKEND HEALTH
    // =========================================================

    async function checkBackend() {

        try {

            const response =
                await fetch("/api/health");

            const data =
                await response.json();

            if (response.ok && data.success) {

                setText(
                    "backendStatus",
                    "BACKEND ONLINE"
                );

            } else {

                setText(
                    "backendStatus",
                    "BACKEND ERROR"
                );
            }

        } catch (error) {

            console.error(
                "Backend health error:",
                error
            );

            setText(
                "backendStatus",
                "BACKEND OFFLINE"
            );
        }
    }


    checkBackend();


    // =========================================================
    // USERNAME SCANNER
    // =========================================================

    const scanBtn =
        $("scanBtn");

    const usernameInput =
        $("username");


    if (scanBtn && usernameInput) {

        scanBtn.addEventListener(
            "click",
            startUsernameScan
        );


        usernameInput.addEventListener(
            "keydown",
            function(event) {

                if (event.key === "Enter") {
                    startUsernameScan();
                }

            }
        );

    }


    async function startUsernameScan() {

        const username =
            usernameInput.value.trim();


        if (!username) {

            showToast(
                "INPUT REQUIRED",
                "Enter a username before starting the scan."
            );

            usernameInput.focus();

            return;
        }


        const validUsername =
            /^[A-Za-z0-9._-]+$/;


        if (!validUsername.test(username)) {

            showToast(
                "INVALID USERNAME",
                "Use letters, numbers, dots, underscores or hyphens."
            );

            return;
        }


        scanBtn.disabled = true;

        scanBtn.innerHTML =
            "SCANNING <span>...</span>";


        const progress =
            $("scanProgress");

        const progressBar =
            $("scanProgressBar");

        const progressText =
            $("scanProgressText");

        const scanCurrent =
            $("scanCurrent");


        if (progress) {
            progress.classList.remove("hidden");
        }


        if (progressBar) {
            progressBar.style.width = "5%";
        }


        if (progressText) {
            progressText.textContent =
                "INITIALIZING";
        }


        if (scanCurrent) {
            scanCurrent.textContent =
                "Connecting to intelligence engine...";
        }


        try {

            const response =
                await fetch(
                    "/api/scan", {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            username: username
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Scan failed."
                );
            }


            // Animate progress
            if (progressBar) {
                progressBar.style.width = "100%";
            }

            if (progressText) {
                progressText.textContent =
                    data.total + " / " + data.total;
            }

            if (scanCurrent) {
                scanCurrent.textContent =
                    "Scan completed successfully.";
            }


            displayUsernameResults(data);


            showToast(
                "SCAN COMPLETE",
                data.found +
                " public profiles found across " +
                data.total +
                " platforms."
            );


        } catch (error) {

            console.error(
                "Username scan error:",
                error
            );

            showToast(
                "SCAN ERROR",
                error.message
            );

        } finally {

            scanBtn.disabled = false;

            scanBtn.innerHTML =
                '<span class="btn-icon">⌁</span>' +
                ' START SCAN ' +
                '<span class="btn-arrow">→</span>';

        }

    }


    function displayUsernameResults(data) {

        setText(
            "total",
            data.total
        );

        setText(
            "found",
            data.found
        );

        setText(
            "blocked",
            data.blocked
        );

        setText(
            "notFound",
            data.not_found
        );

        setText(
            "resultUsername",
            data.username
        );

        setText(
            "score",
            data.score
        );

        setText(
            "risk",
            data.risk
        );

        setText(
            "scanTime",
            data.time
        );


        setText(
            "resultCount",
            data.total + " PLATFORMS"
        );


        const results =
            $("results");


        if (!results) {
            return;
        }


        results.innerHTML = "";


        data.results.forEach(
            function(result, index) {

                const card =
                    document.createElement("div");


                card.className =
                    "result-card";


                card.style.animationDelay =
                    (index * 0.05) + "s";


                let statusClass =
                    "status-unable";


                if (result.status === "FOUND") {
                    statusClass = "status-found";
                } else if (
                    result.status === "BLOCKED"
                ) {
                    statusClass = "status-blocked";
                } else if (
                    result.status === "NOT FOUND"
                ) {
                    statusClass = "status-not-found";
                }


                card.innerHTML = `

                    <div>

                        <div class="result-platform">
                            ${escapeHTML(result.platform)}
                        </div>

                        <div class="result-url">
                            ${escapeHTML(result.url)}
                        </div>

                    </div>

                    <div class="result-status ${statusClass}">
                        ${escapeHTML(result.status)}
                    </div>

                    <div class="result-code">
                        ${result.code || "—"}
                    </div>

                    <a
                        class="result-link"
                        href="${escapeHTML(result.url)}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        OPEN
                    </a>

                `;


                results.appendChild(card);

            }
        );

    }


    // =========================================================
    // PORT SCANNER
    // =========================================================

    const portScanBtn =
        $("portScanBtn");


    if (portScanBtn) {

        portScanBtn.addEventListener(
            "click",
            startPortScan
        );

    }


    async function startPortScan() {

        const target =
            $("portTarget").value.trim();


        if (!target) {

            showToast(
                "TARGET REQUIRED",
                "Enter an IP address or hostname."
            );

            return;
        }


        portScanBtn.disabled = true;

        portScanBtn.textContent =
            "SCANNING...";


        try {

            const response =
                await fetch(
                    "/api/port-scan", {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            target: target
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Port scan failed."
                );
            }


            setText(
                "openPorts",
                data.open
            );

            setText(
                "closedPorts",
                data.closed
            );

            setText(
                "filteredPorts",
                data.filtered
            );

            setText(
                "totalPorts",
                data.total
            );


            displayPortResults(
                data.results
            );


            showToast(
                "PORT SCAN COMPLETE",
                data.open +
                " open ports detected on " +
                data.resolved_ip
            );


        } catch (error) {

            console.error(
                "Port scanner error:",
                error
            );

            showToast(
                "PORT SCAN ERROR",
                error.message
            );

        } finally {

            portScanBtn.disabled = false;

            portScanBtn.innerHTML =
                'SCAN PORTS <span>→</span>';

        }

    }


    function displayPortResults(results) {

        const container =
            $("portResults");


        if (!container) {
            return;
        }


        container.innerHTML = "";


        results.forEach(
            function(item) {

                const row =
                    document.createElement("div");


                row.className =
                    "port-row";


                let stateClass =
                    "port-closed";


                if (item.state === "OPEN") {
                    stateClass = "port-open";
                } else if (
                    item.state === "FILTERED"
                ) {
                    stateClass = "port-filtered";
                }


                row.innerHTML = `

                    <div class="port-number">
                        ${item.port}
                    </div>

                    <div class="port-service">
                        ${escapeHTML(item.service)}
                    </div>

                    <div class="port-state ${stateClass}">
                        ${escapeHTML(item.state)}
                    </div>

                `;


                container.appendChild(row);

            }
        );

    }


    // =========================================================
    // LOG ANALYZER
    // =========================================================

    const analyzeLogBtn =
        $("analyzeLogBtn");


    if (analyzeLogBtn) {

        analyzeLogBtn.addEventListener(
            "click",
            analyzeLogs
        );

    }


    async function analyzeLogs() {

        const logs =
            $("logInput").value;


        if (!logs.trim()) {

            showToast(
                "LOG DATA REQUIRED",
                "Paste some security logs first."
            );

            return;
        }


        analyzeLogBtn.disabled = true;

        analyzeLogBtn.textContent =
            "ANALYZING...";


        try {

            const response =
                await fetch(
                    "/api/log-analyze", {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            logs: logs
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Log analysis failed."
                );
            }


            setText(
                "logLines",
                data.total_lines
            );

            setText(
                "logFailed",
                data.failed
            );

            setText(
                "logErrors",
                data.errors
            );

            setText(
                "logWarnings",
                data.warnings
            );

            setText(
                "logSuspicious",
                data.suspicious
            );

            setText(
                "logRisk",
                data.risk
            );


            displayLogResults(
                data.matches
            );


            showToast(
                "LOG ANALYSIS COMPLETE",
                data.suspicious +
                " suspicious events detected."
            );


        } catch (error) {

            console.error(
                "Log analyzer error:",
                error
            );

            showToast(
                "LOG ANALYSIS ERROR",
                error.message
            );

        } finally {

            analyzeLogBtn.disabled = false;

            analyzeLogBtn.innerHTML =
                'ANALYZE LOGS <span>→</span>';

        }

    }


    function displayLogResults(matches) {

        const container =
            $("logResults");


        if (!container) {
            return;
        }


        container.innerHTML = "";


        if (!matches || matches.length === 0) {

            container.innerHTML = `

                <div class="empty-state">

                    <div class="empty-icon">
                        ✓
                    </div>

                    <p>
                        NO SUSPICIOUS EVENTS DETECTED
                    </p>

                    <small>
                        No matching security patterns were found.
                    </small>

                </div>

            `;

            return;
        }


        matches.forEach(
            function(item) {

                const event =
                    document.createElement("div");


                event.className =
                    "log-event";


                event.textContent =
                    item.message;


                container.appendChild(event);

            }
        );

    }


    // =========================================================
    // IP LOOKUP
    // =========================================================

    const ipLookupBtn =
        $("ipLookupBtn");


    if (ipLookupBtn) {

        ipLookupBtn.addEventListener(
            "click",
            lookupIP
        );

    }


    async function lookupIP() {

        const ip =
            $("ipInput").value.trim();


        if (!ip) {

            showToast(
                "IP REQUIRED",
                "Enter an IP address."
            );

            return;
        }


        ipLookupBtn.disabled = true;

        ipLookupBtn.textContent =
            "LOOKING UP...";


        try {

            const response =
                await fetch(
                    "/api/ip", {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            ip: ip
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "IP lookup failed."
                );
            }


            setText(
                "ipValue",
                data.ip
            );

            setText(
                "ispValue",
                data.isp
            );

            setText(
                "locationValue",
                data.city +
                ", " +
                data.region
            );

            setText(
                "countryValue",
                data.country
            );

            setText(
                "asnValue",
                data.asn
            );

            setText(
                "timezoneValue",
                data.timezone
            );

            setText(
                "latitudeValue",
                data.latitude
            );

            setText(
                "longitudeValue",
                data.longitude
            );


            showToast(
                "IP LOOKUP COMPLETE",
                "Public IP intelligence retrieved successfully."
            );


        } catch (error) {

            console.error(
                "IP lookup error:",
                error
            );

            showToast(
                "IP LOOKUP ERROR",
                error.message
            );

        } finally {

            ipLookupBtn.disabled = false;

            ipLookupBtn.innerHTML =
                'LOOKUP IP <span>→</span>';

        }

    }


    // =========================================================
    // INITIAL MESSAGE
    // =========================================================

    console.log(
        "All frontend modules initialized."
    );

});