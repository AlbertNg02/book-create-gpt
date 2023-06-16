function downloadMarkdownFile() {
    var outputText = document.getElementById("answer").innerText;
    var blob = new Blob([outputText], { type: "text/markdown" });
    var anchor = document.createElement("a");
    anchor.download = "output.md";
    anchor.href = window.URL.createObjectURL(blob);
    anchor.style.display = "none";
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
    window.URL.revokeObjectURL(anchor.href); // Clean up the object URL
}
