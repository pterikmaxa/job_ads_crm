document.addEventListener("DOMContentLoaded", function () {
    function removeRelatedButtons(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        const wrapper = field.closest(".related-widget-wrapper");
        if (!wrapper) return;

        wrapper.querySelectorAll(".related-widget-wrapper-link").forEach(function (link) {
            link.remove();
        });
    }

    removeRelatedButtons("id_country");

    const specializationInput = document.getElementById("id_specialization");
    const technologyChoice = document.getElementById("id_technology_choice");

    if (specializationInput && technologyChoice) {
        const choiceRow = technologyChoice.closest(".form-row");

        const wrapper = document.createElement("span");
        wrapper.className = "technology-choice-inline";

        const label = document.createElement("span");
        label.textContent = "Технология:";
        label.className = "technology-choice-label";

        const addButton = document.createElement("button");
        addButton.type = "button";
        addButton.textContent = "+";
        addButton.className = "technology-add-btn";

        technologyChoice.parentNode.insertBefore(wrapper, technologyChoice);
        wrapper.appendChild(label);
        wrapper.appendChild(technologyChoice);
        wrapper.appendChild(addButton);

        specializationInput.parentNode.appendChild(wrapper);

        if (choiceRow) {
            choiceRow.remove();
        }

        addButton.addEventListener("click", function () {
            const selectedTechnology = technologyChoice.value;
            if (!selectedTechnology) return;

            const currentValue = specializationInput.value || "";

            if (currentValue.trim() === "") {
                specializationInput.value = selectedTechnology;
            } else {
                specializationInput.value = currentValue + " | " + selectedTechnology;
            }

            specializationInput.dispatchEvent(new Event("change", { bubbles: true }));
            specializationInput.focus();
        });
    }
});
