document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("submitTest").addEventListener("click", function () {
        fetch("https://job-test-project.onrender.com/submit_test", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_id: "123", test_results: "测试数据" })
        })
        .then(response => response.json())
        .then(data => console.log("Success:", data))
        .catch(error => console.error("Error:", error));
    });
});