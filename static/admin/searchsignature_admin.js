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

    removeRelatedButtons("id_job_site");
    removeRelatedButtons("id_country");

    const technologyInput = document.getElementById("id_technology");
    const technologyChoice = document.getElementById("id_technology_choice");

    if (technologyInput && technologyChoice) {
        const inputRow = technologyInput.closest(".form-row");
        const choiceRow = technologyChoice.closest(".form-row");

        if (inputRow && choiceRow) {
            const choiceWrapper = document.createElement("span");
            choiceWrapper.className = "technology-choice-inline";

            const label = document.createElement("span");
            label.textContent = "Выбрать из списка:";
            label.className = "technology-choice-label";

            technologyChoice.parentNode.insertBefore(choiceWrapper, technologyChoice);
            choiceWrapper.appendChild(label);
            choiceWrapper.appendChild(technologyChoice);

            const inputContainer = technologyInput.parentNode;
            inputContainer.appendChild(choiceWrapper);

            choiceRow.remove();
        }

        technologyChoice.addEventListener("change", function () {
            if (technologyChoice.value) {
                technologyInput.value = technologyChoice.value;
                technologyInput.dispatchEvent(new Event("change", { bubbles: true }));
            }
        });
    }
});
