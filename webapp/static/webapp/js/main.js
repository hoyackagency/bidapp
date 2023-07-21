// myproject/webapp/static/webapp/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    var feed_entry_id = document.getElementById('data-id').textContent;

    function sendStatus(status) {
        fetch('/thumbsdown/', {
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
                document.getElementById('card-title').textContent = data.title;
                document.getElementById('card-content').textContent = data.content;
                feed_entry_id = data.id;  // update feed entry id
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
});
