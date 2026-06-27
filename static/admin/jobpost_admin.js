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
});
