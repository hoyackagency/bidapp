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

document.getElementById("recycle-btn").onclick = function() {
    fetch(`/view?recycle=true&feed_entry_id=${feed_entry_id}`)
    .then(response => response.json())
    .then(data => {
        feed_entry_id = data.id;  // update the global variable with the new id

        // update the HTML elements with the new data
        document.getElementById("card-title").textContent = data.title;
        document.getElementById("card-content").textContent = data.content;
        document.getElementById("card-feed").textContent = "Feed: " + data.feed.feed_name;
        // document.getElementById("card-published_date").textContent = "Published Date: " + data.published_date;
        document.getElementById("card-pay_range").textContent = "Pay Range: " + data.pay_range;
        document.getElementById("card-job_type").textContent = "Job Type: " + data.job_type;
        document.getElementById("card-category").textContent = "Category: " + data.category;
        
        // split the skills string into an array of skills
        let skillsArray = data.skills.split(',');
        // create a badge for each skill
        let badgesHTML = skillsArray.map(skill => `<span class="badge badge-pill badge-primary">${skill.trim()}</span>`).join(' ');
        // set the HTML of the skills element to the badges
        document.getElementById("card-skills").innerHTML = "Skills: " + badgesHTML;
        
        document.getElementById("card-country").textContent = "Country: " + data.country;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}