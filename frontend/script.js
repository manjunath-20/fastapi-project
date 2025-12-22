async function uploadFile() {
    let fileInput = document.getElementById("pdfFile");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please choose a PDF first");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    let response = await fetch("http://127.0.0.1:8000/summarize", {
        method: "POST",
        body: formData
    });

    let result = await response.json();

    document.getElementById("output").innerText = result.summary;
}