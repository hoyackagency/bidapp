// main.js

function sendStatus(status) {
    fetch(thumbs_down_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `id=${feed_entry_id}&status=${status}`,
    }).then(response => {
        console.log(response);
        location.reload();  // reload the page
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

document.getElementById("thumbsdown").onclick = function() {
    sendStatus('decline');
}

document.getElementById("thumbsup").onclick = function() {
    sendStatus('accept');
}

document.getElementById("recycle").onclick = function() {
    fetch(`http://localhost:8000/view?recycle=true&feed_entry_id=${feed_entry_id}`)
        .then(response => response.json())
        .then(data => {
            var titleElement = document.getElementById('card-title');
            titleElement.textContent = data.title;
            titleElement.href = data.link;  // set the href to the new URL
            document.getElementById('card-content').textContent = data.content;
            feed_entry_id = data.id;  // update feed entry id
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
