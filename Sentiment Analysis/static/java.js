
    function analyzeSentiment() {
        // Get the text input value
        var text = document.getElementById("text").value;

        // Create a new XMLHttpRequest object
        var xhr = new XMLHttpRequest();

        // Configure the AJAX request
        xhr.open("POST", "/", true);
        xhr.setRequestHeader("Content-Type", "application/json");

        // Define what to do on response
        xhr.onload = function () {
            if (xhr.status == 200) {
                // Parse the JSON response
                var response = JSON.parse(xhr.responseText);

                // Update the sentiment result dynamically
                if (response.sentiment) {
                    var sentimentText = response.sentiment == 'Positive' ? 'green' : 'red';
                    var fontSize = response.sentiment == 'Positive' ? '24px' : '20px';

                    document.getElementById("result").innerHTML = `
                        <h2>Sentiment Result</h2>
                        <p><strong>Text:</strong> ${response.text}</p>
                        <p><strong>Sentiment:</strong> 
                            <span style="color: ${sentimentText}; font-size: ${fontSize};">${response.sentiment}</span>
                        </p>
                    `;
                }
            }
        };

        // Send the request with the text data
        xhr.send(JSON.stringify({ text: text }));
    }
