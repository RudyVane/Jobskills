<!DOCTYPE html>
<html>
<head>
<title>Vaardigheden uit vacaturetekst filteren</title>
</head>
<body>

<form action="" method="post">
<p>vacaturetekst</p>
<textarea name="vacaturetekst" rows="10" cols="50" placeholder="voer hier de vacaturetekst in"></textarea>
<p>cv</p>
<textarea name="cv" rows="10" cols="50" placeholder="voer hier je cv in"></textarea>

<br>
<input type="submit" value="Submit">
</form>
<?php

// Your OpenAI API key
$api_key = "";

// Function to make the API call using cURL
function call_openai_api($api_key, $data) {
    $url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'; 
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
if (isset($_POST['vacaturetekst'])) {
    $vacaturetekst = $_POST['vacaturetekst'];
	$cv = $_POST['cv'];
    // Maak een API-aanroep naar de AI-service
    $data = [
        'prompt' => "Please read the job offer and the candidate's CV provided below. Extract the required skills and tools from each text and compare them. Finally, return a table of required skills and tools(use just one word for a skill or tool), a table of resume skills and tools (use just one word for a skill or tool) and a table of matching skills and tools found in both texts(use just one word for a skill or tool):job offer:\n" . $vacaturetekst . "resume:\n" . $cv ,
        'temperature' => 0,
        'max_tokens' => 1500,
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
            if (isset($response['choices'][0]['text'])) {
                echo "<h2>Resultaat:</h2>";
                echo nl2br($response['choices'][0]['text']);
            } else {
                echo "Failed to extract skills.";
            }
        }
    }
}
?>
</body>
</html>
