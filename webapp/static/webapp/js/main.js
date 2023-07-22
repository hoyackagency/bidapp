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
            document.getElementById('card-title').textContent = data.title;
            document.getElementById('card-title').href = data.link;
            document.getElementById('card-content').textContent = data.content;
            document.getElementById('card-feed').textContent = "Feed: " + data.feed.feed_name;
            document.getElementById('card-published_date').textContent = "Published Date: " + data.published_date;
            document.getElementById('card-pay_range').textContent = "Pay Range: " + data.pay_range;
            document.getElementById('card-job_type').textContent = "Job Type: " + data.job_type;
            document.getElementById('card-category').textContent = "Category: " + data.category;
            document.getElementById('card-skills').textContent = "Skills: " + data.skills;
            document.getElementById('card-country').textContent = "Country: " + data.country;
            feed_entry_id = data.id;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
