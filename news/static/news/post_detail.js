document.addEventListener("DOMContentLoaded", function() {
    const content = document.getElementById('post-content');
    const toggleBtn = document.getElementById('toggle-content');

    const maxWords = 100; // number of words to show initially
    const fullText = content.innerHTML;
    const words = fullText.split(/\s+/);

    if (words.length > maxWords) {
        const shortText = words.slice(0, maxWords).join(' ') + '...';
        content.innerHTML = shortText;

        toggleBtn.style.display = 'inline-block';
        let expanded = false;

        toggleBtn.addEventListener('click', () => {
            if (!expanded) {
                content.innerHTML = fullText;
                toggleBtn.textContent = 'Show less';
            } else {
                content.innerHTML = shortText;
                toggleBtn.textContent = 'Read more';
            }
            expanded = !expanded;
        });
    } else {
        toggleBtn.style.display = 'none';
    }
});