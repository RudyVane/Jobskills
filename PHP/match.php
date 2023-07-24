<!DOCTYPE html>
<html>
<head>
<title>Vaardigheden uit vacaturetekst filteren</title>
</head>
<body>

<form action="" method="post">
<p>vacaturetekst URL:</p>
<input type="url" name="url_vacaturetekst" size = "100" placeholder="voer hier de URL van de vacaturetekst in">
<p>cv</p>
<textarea name="cv" rows="10" cols="50" placeholder="voer hier je cv in"></textarea>

<br>
<input type="submit" value="Submit">
</form>
<?php

// Your OpenAI API key
$api_key = "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"; // Replace with your OpenAI API key

// Function to make the API call using cURL
function call_openai_api($api_key, $data) {
    $url = 'https://api.openai.com/v1/chat/completions';
    $headers = [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $api_key,
    ];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);
    curl_close($ch);

    return json_decode($response, true);
}

// Vraag de gebruiker om tekst in te voeren
if (isset($_POST['url_vacaturetekst'])) {
    $url_vacaturetekst = $_POST['url_vacaturetekst'];
    $cv = $_POST['cv'];

   	// Fetch the HTML content from the URL
$html = file_get_contents($url_vacaturetekst);

// Remove HTML tags to get plain text
$vacaturetekst = strip_tags($html);

    // Maak een API-aanroep naar de AI-service
    $data = [
        'messages' => [
            [
                'role' => 'system',
                'content' => 'Extract the required skills and tools from the following job offer:',
            ],
            [
                'role' => 'user',
                'content' => $vacaturetekst,
            ],
            [
                'role' => 'system',
                'content' => 'and the candidate\'s CV:',
            ],
            [
                'role' => 'user',
                'content' => $cv,
            ],
            [
                'role' => 'system',
                'content' => 'Compare them and return a table of required skills and tools(use just one word for a skill or tool), a table of resume skills and tools (use just one word for a skill or tool), and a table of matching skills and tools found in both texts(use just one word for a skill or tool)',
            ],
        ],
        'temperature' => 0,
        'max_tokens' => 3000,
        'model' => 'gpt-3.5-turbo-16k',
    ];

    $response = call_openai_api($api_key, $data);

    // Controleer op fouten in de reactie
    if (!$response) {
        echo "Failed to communicate with the API.";
    } else {
        if (isset($response['error'])) {
            echo "API Error: " . $response['error']['message'];
        } else {
            // Toon de gegenereerde output
            if (isset($response['choices'][0]['message']['content'])) {
                echo "<h2>Resultaat:</h2>";
                echo nl2br($response['choices'][0]['message']['content']);
            } else {
                echo "Failed to extract skills.";
            }
        }
    }
}
?>
</body>
</html>
