document.addEventListener("DOMContentLoaded", function () {
    // LOGIN FUNCTION
    async function login() {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const response = await fetch("http://localhost:8000/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem("token", data.token);
            window.location.href = "dashboard.html"; // Redirect after login
        } else {
            alert("Login failed: " + data.error);
        }
    }

    // SEARCH FUNCTION
    async function searchNotes() {
        const query = document.getElementById("search").value;
        const response = await fetch(`http://localhost:8000/search-notes/?query=${query}`);
        const data = await response.json();

        const results = document.getElementById("results");
        results.innerHTML = data
            .map(note => `<li>${note.topics} - ${note.course__course_name}</li>`)
            .join("");
    }

    // FETCH COURSES
    async function loadCourses() {
        const response = await fetch("http://localhost:8000/courses/");
        const data = await response.json();
        const courseContainer = document.getElementById("courses");

        courseContainer.innerHTML = data.map(course =>
            `<div class="card"><h3>${course.CourseName}</h3></div>`).join("");
    }

    // NOTE UPLOAD FUNCTION
    async function uploadNote() {
        const courseID = document.getElementById("course_id").value;
        const topics = document.getElementById("topics").value;
        const fileInput = document.getElementById("file");

        const formData = new FormData();
        formData.append("CourseID", courseID);
        formData.append("Topics", topics);
        formData.append("file", fileInput.files[0]);

        const response = await fetch("http://localhost:8000/notes/upload/", {
            method: "POST",
            headers: { "Authorization": "Token " + localStorage.getItem("token") },
            body: formData,
        });

        const data = await response.json();
        if (response.ok) {
            alert("Note uploaded successfully!");
        } else {
            alert("Error: " + data.error);
        }
    }

    // Assign functions to buttons
    if (document.getElementById("loginBtn")) {
        document.getElementById("loginBtn").addEventListener("click", login);
    }
    if (document.getElementById("searchBtn")) {
        document.getElementById("searchBtn").addEventListener("click", searchNotes);
    }
    if (document.getElementById("uploadBtn")) {
        document.getElementById("uploadBtn").addEventListener("click", uploadNote);
    }

    // Load courses if on dashboard
    if (document.getElementById("courses")) {
        loadCourses();
    }
});
