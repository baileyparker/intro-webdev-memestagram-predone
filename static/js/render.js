function renderMeme(canvas) {
    var img = new Image();
    var top_caption = canvas.getAttribute('data-top-caption');
    var bottom_caption = canvas.getAttribute('data-bottom-caption');
    img.onload = function() {
        console.log(canvas);
        canvas.width = img.width;
        canvas.height = img.height;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        ctx.font = "bold 75px Impact";
        ctx.fillStyle = 'white';
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;
        ctx.textAlign = "center";
        ctx.textBaseline = "top";
        ctx.fillText(top_caption, canvas.width/2, 0, canvas.width);
        ctx.strokeText(top_caption, canvas.width/2, 0, canvas.width);
        ctx.textBaseline = "bottom";
        ctx.fillText(bottom_caption, canvas.width/2, canvas.height, canvas.width);
        ctx.strokeText(bottom_caption, canvas.width/2, canvas.height, canvas.width);
    };
    img.src = canvas.getAttribute('data-src');
}

document.addEventListener('DOMContentLoaded', function() {
    var memes = document.getElementsByClassName('meme-render');

    for (var i = 0; i < memes.length; i++) {
        renderMeme(memes[i]);
    }
});
