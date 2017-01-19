function prepareLikeLink(link) {
    link.addEventListener('click', function(e) {
        e.preventDefault();

        var request = new XMLHttpRequest();
        request.open('GET', link.href);
        request.send();

        var countSpan = link.getElementsByClassName('count')[0];
        countSpan.textContent = parseInt(countSpan.textContent) + 1;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var like_links = document.getElementsByClassName('like-link');

    for (var i = 0; i < like_links.length; i++) {
        prepareLikeLink(like_links[i]);
    }
});
