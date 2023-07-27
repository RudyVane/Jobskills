
<?php
class ApiHandler
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

                // Define the data for the API call for the job offer
                $data_job_offer = [
                    'messages' => [
                        [
                            'role' => 'system',
                            'content' => 'Extract the required skills and qualifications from the following job offer. Please focus only on the skills and qualifications directly relevant to the role. Omit general terms and avoid including unrelated words like \'phone,\' \'budget,\' and similar non-skill related terms. Your response should include a unordered list of essential skills and qualifications required for the job, your answer must be in dutch:',
                        ],
                        [
                            'role' => 'user',
                            'content' => $jobOfferText,
                        ],
                    ],
                    'temperature' => 0,
                    'max_tokens' => 3000,
                    'model' => 'gpt-3.5-turbo-16k',
                ];

                // Make the API call for the job offer
                $response_job_offer = $this->call_openai_api($data_job_offer);
	
				// Get the matching skills from the API response
				$job = $response_job_offer['choices'][0]['message']['content'];

				// Count the skills in the matching skills result
				$count_job = count(explode(" ", strip_tags($job)));
                // Define the data for the API call for the CV
                $data_cv = [
                    'messages' => [
                        [
                            'role' => 'system',
                            'content' => 'Extract the jobskills from the candidate\'s CV (use one word per skill) as an unordered list in dutch:',
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

                // Make the API call for the CV
                $response_cv = $this->call_openai_api($data_cv);

                // Make an API call to compare job offer and CV responses
			$data_match = [
				'messages' => [
            [
                'role' => 'system',
                'content' => 'Compare the skills in the job offer and CV and return the matching skills as a list in Dutch, only return a unordered list of matching skills, no extra text:',
            ],
            [
                'role' => 'user',
                'content' => $response_job_offer['choices'][0]['message']['content'],
            ],
            [
                'role' => 'system',
                'content' => 'CV',
            ],
            [
                'role' => 'user',
                'content' => $response_cv['choices'][0]['message']['content'],
            ],
        ],
        'temperature' => 0,
        'max_tokens' => 3000,
        'model' => 'gpt-3.5-turbo-16k',
    ];

    $response_match = $this->call_openai_api($data_match);
	
	// Get the matching skills from the API response
	$matching_skills_result = $response_match['choices'][0]['message']['content'];

	// Count the skills in the matching skills result
	$count_matching_skills = count(explode(" ", strip_tags($matching_skills_result)));
	$percentage = $count_matching_skills / $count_job *100;
    
    // Store the data in the session to access it in the results page
    session_start();
    $_SESSION['job_offer'] = $response_job_offer['choices'][0]['message']['content'];
    $_SESSION['cv'] = $response_cv['choices'][0]['message']['content'];
    $_SESSION['matching_skills'] = $response_match['choices'][0]['message']['content'];
	$_SESSION['match'] = $percentage . "%";
				
                // Redirect to the results page to display the API response
                header("Location: results.php");
                exit();
            } else {
                // Als de vereiste velden niet zijn ingevuld, terugsturen naar het formulier met een foutmelding
                header("Location: index.php?error=missing_fields");
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
