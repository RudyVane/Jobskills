
<?php
class ApiHandler1
{
    // Function to check if the given text is a URL
    private function isUrl($text)
    { 
        // Use a regular expression to check the URL
        $pattern = '/^(https?|ftp):\/\/[^\s\/$.?#].[^\s]*$/i';

        // Use preg_match to compare the text with the pattern
        return preg_match($pattern, $text);
    }

    public function handleFormSubmission()
    {
        // Controleer of het formulier is ingediend
        if ($_SERVER["REQUEST_METHOD"] === "POST") {
            // Controleer of de vereiste velden zijn ingevuld
            if (isset($_POST['job']) && isset($_POST['cv'])) {
                // Haal de ingediende gegevens op
                $job = $_POST['job'];
                $cv = $_POST['cv'];

                // Controleer of $job een URL is
                if ($this->isUrl($job)) {
                    // Text processing for job offer and CV
                    $jobOfferText = $this->getPlainTextFromUrl($job);
                } else {
                    $jobOfferText = $job;
                }

                

                // Make an API call to compare job offer and CV responses
			$data_match = [
				'messages' => [
            [
                'role' => 'system',
                'content' => 'Compare the skills in the job offer and CV and write a motivation letter to apply for the job:',
            ],
            [
                'role' => 'user',
                'content' => $jobOfferText,
            ],
            [
                'role' => 'system',
                'content' => 'CV',
            ],
            [
                'role' => 'user',
                'content' => $cv,
            ],
        ],
        'temperature' => 0,
        'max_tokens' => 3000,
        'model' => 'gpt-3.5-turbo-16k',
    ];

    $response_match = $this->call_openai_api($data_match);
	
	
    
    // Store the data in the session to access it in the results page
    session_start();
    
	$_SESSION['motivation'] = $response_match['choices'][0]['message']['content'];
				
                // Redirect to the results page to display the API response
                header("Location: letter.php");
                exit();
            } else {
                // Als de vereiste velden niet zijn ingevuld, terugsturen naar het formulier met een foutmelding
                header("Location: motivatie.php?error=missing_fields");
                exit();
            }
        }
    }

    // Function to read the API key from the file
    private function read_api_key()
    {
        $file = "api.txt"; // Replace with the path to your api_key.txt file
        $api_key = trim(file_get_contents($file));
        return $api_key;
    }

    // Function to make the API call using cURL
    private function call_openai_api($data)
    {
        $api_key = $this->read_api_key();
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
        if ($response === false) {
            // Display cURL error if any
            echo 'cURL error: ' . curl_error($ch);
        }
        curl_close($ch);

        return json_decode($response, true);
    }

    // Function to get plain text from a URL and remove HTML tags
    private function getPlainTextFromUrl($url)
    {
        $html = file_get_contents($url);
        return strip_tags($html);
    }
}
?>
