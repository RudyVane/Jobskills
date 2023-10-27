<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $jobOffer = $_POST['job_offer'];
    $cv = $_POST['cv'];

    // Data for the job offer and CV
    $data = [
        'job_offer' => $jobOffer,
        'cv' => $cv,
    ];

    // Convert the data to JSON
    $jsonData = json_encode($data);

    // Create a cURL request to send the JSON data to the API handler
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://rudy65.privemail.nl/Jobsearch/ApiHandlerDiscord.php');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    // Execute the cURL request
    $response = curl_exec($ch);

    // Close the cURL session
    curl_close($ch);

    // Display the returned JSON
    echo $response;
} else {
    // Display the form to input job offer and CV
    ?>
    <html>
    <head>
        <title>Webhook Form</title>
    </head>
    <body>
        <h1>Enter Job Offer and CV</h1>
        <form method="post">
            <label for="job_offer">Job Offer:</label>
            <textarea name="job_offer" id="job_offer" rows="4" cols="50"></textarea><br>

            <label for="cv">CV:</label>
            <textarea name="cv" id="cv" rows="4" cols="50"></textarea><br>

            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    <?php
}
?>

