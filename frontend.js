document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("submitTest");
    if (button) {
        button.addEventListener("click", submitTest);
    } else {
        console.error("❌ 按钮 `submitTest` 未找到，请检查 HTML 代码！");
    }
});

function submitTest() {
    let keyScore = document.getElementById("keyScore").value;
    let tendencyScore = document.getElementById("tendencyScore").value;
    let detailedScore = document.getElementById("detailedScore").value;
    let confirmScore = document.getElementById("confirmScore").value;

    fetch("https://job-test-project.onrender.com/submit_test", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "123",
            key_score: keyScore,
            tendency_score: tendencyScore,
            detailed_score: detailedScore,
            confirm_score: confirmScore
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("✅ 提交成功:", data);
        document.getElementById("result").innerHTML = `<strong>测试结果：</strong> ${data.message || "提交成功"}`;
    })
    .catch(error => {
        console.error("❌ 提交失败:", error);
        document.getElementById("result").innerHTML = `<strong>错误：</strong> 提交失败，请检查网络连接或稍后重试。`;
    });
}