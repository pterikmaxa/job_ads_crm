document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("input.spin-field").forEach(function (input) {
        if (input.dataset.spinReady === "1") return;
        input.dataset.spinReady = "1";

        const wrapper = document.createElement("span");
        wrapper.className = "spin-wrapper";

        const minus = document.createElement("button");
        minus.type = "button";
        minus.className = "spin-btn";
        minus.textContent = "-";

        const plus = document.createElement("button");
        plus.type = "button";
        plus.className = "spin-btn";
        plus.textContent = "+";

        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(minus);
        wrapper.appendChild(input);
        wrapper.appendChild(plus);

        minus.addEventListener("click", function () {
            const value = parseInt(input.value || "0", 10);
            const min = parseInt(input.getAttribute("min") || "0", 10);
            input.value = Math.max(min, value - 1);
            input.dispatchEvent(new Event("change", { bubbles: true }));
        });

        plus.addEventListener("click", function () {
            const value = parseInt(input.value || "0", 10);
            input.value = value + 1;
            input.dispatchEvent(new Event("change", { bubbles: true }));
        });
    });
});
