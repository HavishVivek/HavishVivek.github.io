window.onload = function() {
    fetch('/list_blogs')
        .then(response => response.json())
        .then(data => {
            const blogsList = document.getElementById('blogs');
            data.blogs.forEach(blog => {
                const li = document.createElement('li');
                li.textContent = blog;
                li.onclick = function() {
                    document.getElementById('user-input').value = 
                        `Tell me about the blog "${blog}"`;
                };
                blogsList.appendChild(li);
            });
        });
};

function sendMessage() {
    // ... (rest of the JavaScript code)
}