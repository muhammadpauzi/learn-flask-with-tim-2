const likeButtons = document.querySelectorAll('.btn-like');

likeButtons.forEach(likeButton => {
    likeButton.addEventListener('click', like)
});

async function like() {
    try {
        const { postId } = this.dataset;
        const likeCount = this.firstElementChild;
        // send request
        const res = await fetch(`like-post/${postId}`, { method: 'POST' });
        const data = await res.json();
        // set like count
        likeCount.textContent = data.likes;
        // set thumb icon
        this.textContent = data.liked ? '👎 ' : '👍 ';
        // add like count element to like button
        this.appendChild(likeCount);
    } catch (err) {
        alert('Cannot like, Something\'s went wrong.')
        console.log(err);
    }
}