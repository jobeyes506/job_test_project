document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("payButton").addEventListener("click", function () {
        fetch("https://job-test-project.onrender.com/submit_payment", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: "123456",
                amount: 9.00,
                status: "SUCCESS",
                transaction_id: "TEST123456"
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Payment Success:", data);
            alert("支付成功！可以进行测试");
            localStorage.setItem("isPaid", "true"); // 本地存储支付状态
            window.location.reload(); // 刷新页面，进入测试流程
        })
        .catch(error => console.error("Payment Error:", error));
    });

    // 检查支付状态
    if (localStorage.getItem("isPaid") === "true") {
        document.getElementById("testSection").style.display = "block"; // 显示测试内容
    }
});