document.addEventListener("DOMContentLoaded", () => {
    checkAuthStatus();
    document.getElementById("listFilesBtn").addEventListener("click", listFiles);
});

async function checkAuthStatus() {
    try {
        let response = await fetch("/auth-status");
        let data = await response.json();
        if (data.loggedIn) {
            document.getElementById("userMessage").textContent = `Welcome, ${data.user}`;
            document.getElementById("logoutBtn").classList.remove("hidden");
        } else {
            document.getElementById("userMessage").innerHTML = 'Not logged in. <a href="/login">Login</a>';
            document.getElementById("logoutBtn").classList.add("hidden");
        }
    } catch (error) {
        console.error("Error checking auth status:", error);
    }
}

async function logout() {
    try {
        // Using GET for logout because our Flask route accepts GET
        await fetch("/logout", { method: "GET" });
        window.location.reload();
    } catch (error) {
        console.error("Logout failed:", error);
    }
}

async function uploadFile() {
    let fileInput = document.getElementById("fileInput").files[0];
    if (!fileInput) {
        alert("Please select a file to upload.");
        return;
    }
    let formData = new FormData();
    formData.append("file", fileInput);
    try {
        let response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        let result = await response.json();
        alert(result.message || result.error);
        listFiles();  // Refresh file list after upload
    } catch (error) {
        console.error("Upload failed:", error);
        alert("Upload failed.");
    }
}

async function listFiles() {
    try {
        let response = await fetch("/files");
        let files = await response.json();
        let fileList = document.getElementById("fileList");
        fileList.innerHTML = "";
        files.forEach(file => {
            let li = document.createElement("li");
            li.textContent = file + " ";
            // Create Download button
            let downloadBtn = document.createElement("button");
            downloadBtn.textContent = "Download";
            downloadBtn.onclick = () => downloadFile(file);
            li.appendChild(downloadBtn);
            // Create Delete button
            let deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.onclick = () => deleteFile(file);
            li.appendChild(deleteBtn);
            fileList.appendChild(li);
        });
    } catch (error) {
        console.error("Error listing files:", error);
    }
}

async function downloadFile(fileName) {
    if (!fileName) {
        fileName = document.getElementById("downloadFileName").value;
        if (!fileName) {
            alert("Please enter a file name.");
            return;
        }
    }
    try {
        let response = await fetch(`/download?file_name=${encodeURIComponent(fileName)}`);
        let data = await response.json();
        if (data.file_url) {
            window.open(data.file_url, "_blank");
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error("Error downloading file:", error);
    }
}

async function deleteFile(fileName) {
    if (!fileName) {
        fileName = document.getElementById("deleteFileName").value;
        if (!fileName) {
            alert("Please enter a file name.");
            return;
        }
    }
    try {
        let response = await fetch("/delete", {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ file_name: fileName })
        });
        let result = await response.json();
        alert(result.message || result.error);
        listFiles();  // Refresh file list after deletion
    } catch (error) {
        console.error("Deletion failed:", error);
        alert("Failed to delete file.");
    }
}
