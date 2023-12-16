document.getElementById('article-form').addEventListener('submit', function(event) {
    var articleLink = document.getElementById('article_link').value;
    if (!articleLink) {
        event.preventDefault();
        alert('Please enter an article link.');
    } else if (!/^https?:\/\//i.test(articleLink)) {
        event.preventDefault();
        alert('Please enter a valid URL. It should start with "http://" or "https://".');
    }
});