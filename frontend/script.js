async function uploadFile() {
    let fileInput = document.getElementById("pdfFile");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please choose a PDF first");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    let response = await fetch("https://fastapi-backend-emfc.onrender.com", {
        method: "POST",
        body: formData
    });

    let result = await response.json();

    document.getElementById("output").innerText = result.summary;
}