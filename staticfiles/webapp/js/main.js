// main.js

function sendStatus(status) {
    fetch(thumbs_updown_url, {
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

function toBadges(value) {
    // split the value into an array of skills
    let skillsArray = value.split(',');

    // create a badge for each skill
    let badgesHTML = skillsArray.map(skill => `<span class="badge badge-pill badge-primary">${skill.trim()}</span>`).join(' ');

    // return the HTML string of badges
    return badgesHTML;
}

// use this function to set the badges HTML in the recycle function
document.getElementById("recycle-btn").onclick = function() {
    fetch(`/view?recycle=true&feed_entry_id=${feed_entry_id}`)
    .then(response => response.json())
    .then(data => {
        feed_entry_id = data.id;  // update the global variable with the new id

        // update the HTML elements with the new data
        document.getElementById("card-title").textContent = data.title;
        document.getElementById("card-content").textContent = data.content;
        document.getElementById("card-feed-value").textContent = data.feed.feed_name;
        document.getElementById("card-pay_range-value").textContent = data.pay_range;
        document.getElementById("card-job_type-value").textContent = data.job_type;
        document.getElementById("card-category-value").textContent = data.category;
        var skillsHtml = toBadges(data.skills);
        document.getElementById("card-skills-value").innerHTML = skillsHtml;
        document.getElementById("card-country-value").textContent = data.country;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
